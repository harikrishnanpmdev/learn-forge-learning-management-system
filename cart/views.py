from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from accounts.models import Course, Section, Quiz
from cart.models import Cart, Order, OrderItem, Enrollment, Lesson, LessonCompletion, Certificate
from django.conf import settings
import razorpay, uuid
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from playwright.sync_api import sync_playwright

class AddToCart(LoginRequiredMixin, View):
    
    def get(self, request, i):
        if request.user.want_to_join_as == "teacher":
            messages.warning(request, "Instructors Cannot Add Courses to Cart")
            return redirect("accounts:course_detail", i=i)
        course = get_object_or_404(Course, id=i)
        cart, created = Cart.objects.get_or_create(user=request.user, course=course)

        if created:
            messages.success(request, f"{course.title} has been added to your cart.")
        else:
            messages.warning(request, f"{course.title} is already in your cart.")

        return redirect('cart:cartview')
    
class CartView(LoginRequiredMixin, View):

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user).select_related('course')
        # Django performs a SQL JOIN and retrieves both the cart items and their related course details in one query.
        total_price = 0
        total_old_price = 0
        total_lessons = 0

        for item in cart_items:
            total_price += item.course.price
            total_lessons += item.course.lessons
            if item.course.old_price:
                total_old_price += item.course.old_price
            else:
                total_old_price += item.course.price
        
        total_savings = total_old_price - total_price
        discount_percentage = 0

        if total_old_price > 0:
            discount_percentage = round((total_savings / total_old_price) * 100)

        context ={
            'cart_items': cart_items,
            'total_price': total_price,
            'total_old_price': total_old_price,
            'total_savings': total_savings,
            'discount_percentage': discount_percentage,
            'total_lessons': total_lessons,
        }
        return render(request, 'cart.html', context)
    
class RemoveFromCart(LoginRequiredMixin, View):

    def get(self, request, i):
        cart_item = get_object_or_404(Cart, id=i, user=request.user)
        course_title = cart_item.course.title
        cart_item.delete()
        messages.success(request, f"{course_title} has been removed from your cart.")
        return redirect('cart:cartview')
    
class CheckoutView(LoginRequiredMixin, View):

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user).select_related('course')

        if not cart_items.exists():
            messages.warning(request, "Your cart is empty. Please add courses to your cart before proceeding to checkout.")
            return redirect('cart:cartview')
        
        total_amount = sum(item.course.price for item in cart_items)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

        razorpay_order = client.order.create({
            "amount": int(total_amount * 100),
            "currency": "INR",
            "payment_capture": 1
        })

        order = Order.objects.create(
            user=request.user,
            order_amount=total_amount,
            razorpay_order_id=razorpay_order["id"],
            status="pending"
        )

        context = {
            "order": order,
            "cart_items": cart_items,
            "razorpay_order_id": razorpay_order["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": total_amount,
        }
        return render(request, "checkout.html", context)
    
class PaymentSuccessView(LoginRequiredMixin, View):

    def get(self, request):
        payment_id = request.GET.get('payment_id')
        order_id = request.GET.get('order_id')
        signature = request.GET.get('signature')

        if not all([payment_id,order_id,signature]):
            messages.error(request, "Invalid payment response.")
            return redirect('cart:cartview')
        
        order = get_object_or_404(Order, user=request.user, razorpay_order_id=order_id)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,

                'razorpay_payment_id': payment_id,

                'razorpay_signature': signature
            })
        except Exception as e:
            print("RAZORPAY ERROR:", e)
            order.status = 'failed'
            order.save()
            messages.error(request, f"Payment verification failed: {e}")
            return redirect('cart:cartview')
        
        order.razorpay_payment_id = payment_id
        order.razorpay_signature = signature
        order.status = 'success'
        order.is_ordered = True
        order.save()

        cart_items = Cart.objects.filter(user=request.user).select_related('course')

        for item in cart_items:
            OrderItem.objects.create(order=order, course=item.course, price=item.course.price)
            Enrollment.objects.get_or_create(student=request.user, course=item.course)
        cart_items.delete()
        messages.success(request, "Payment completed successfully. Courses added to your account.")
        return redirect('cart:my_courses')
    
class MyCoursesView(LoginRequiredMixin, View):
    
    def get(self, request):
        courses = Enrollment.objects.filter(student=request.user).select_related('course').order_by('-enrolled_date')

        for item in courses:
            total_lessons = Lesson.objects.filter(section__course=item.course).count()
            completed_lessons = LessonCompletion.objects.filter(student=request.user, lesson__section__course=item.course).count()
            progress_percentage = 0
            if total_lessons > 0:
                progress_percentage = round((completed_lessons / total_lessons) * 100)

            item.progress_percentage = progress_percentage

        context = {'courses': courses}
        return render(request, 'my_courses.html', context)
    
class CourseLearningView(LoginRequiredMixin, View):

    def get(self, request, i):
        course = get_object_or_404(Course, id=i)
        enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
        if not enrolled:
            messages.error(request, "You are not enrolled in this course.")
            return redirect('accounts:coursedetails',i)
        
        lessons = Lesson.objects.filter(section__course=course).select_related('section')
        sections = Section.objects.filter(course=course).prefetch_related('lessons')
        lesson_id = request.GET.get('lesson')

        if lesson_id:
            current_lesson = get_object_or_404(Lesson, id=lesson_id, section__course=course)
        else:
            current_lesson = lessons.first()
        
        completed_lessons = LessonCompletion.objects.filter(student=request.user, lesson__section__course=course)
        completed_ids = list(completed_lessons.values_list('lesson_id',flat=True))
        # values_list() retrieves only the specified field instead of the entire object.

        total_lessons = lessons.count()
        completed_count = completed_lessons.count()

        if total_lessons > 0:
            progress_percent = round((completed_count / total_lessons) * 100)
        
        quiz = Quiz.objects.filter(course=course, is_active=True).first()

        context = {
            'course': course,
            'sections': sections,
            'lessons': lessons,
            'current_lesson': current_lesson,
            'completed_ids': completed_ids,
            'total_lessons': total_lessons,
            'completed_count': completed_count,
            'progress_percent': progress_percent,
            'quiz': quiz,
        }
        return render(request, 'course_learning.html', context)
    
class CompleteLessonView(LoginRequiredMixin, View):

    def post(self, request, i):
        lesson = get_object_or_404(Lesson, id=i)
        completion, created = LessonCompletion.objects.get_or_create(student=request.user, lesson=lesson)
        course = lesson.section.course
        total_lessons = Lesson.objects.filter(section__course=course).count()
        completed_lessons = LessonCompletion.objects.filter(student=request.user, lesson__section__course=course).count()

        if total_lessons > 0 and completed_lessons == total_lessons:
            Certificate.objects.get_or_create(student=request.user, course=course,
                defaults={
                    'certificate_id': "LF-" + str(uuid.uuid4())[:8].upper()
                }
            )
        return JsonResponse({'success': True,'created': created})

class ResumeLearningView(LoginRequiredMixin, View):

    def get(self, request, i):
        course = get_object_or_404(Course, id=i)
        lessons = Lesson.objects.filter(section__course=course).order_by('lesson_order')
        completed_ids = LessonCompletion.objects.filter(
            student=request.user, lesson__section__course=course).values_list('lesson_id',flat=True)
        
        next_lesson = lessons.exclude(id__in=completed_ids).first()

        if next_lesson:
            return redirect(
                f"/cart/learn_course/{course.id}?lesson={next_lesson.id}"
            )
        
        first_lesson = lessons.first()

        if first_lesson:
            return redirect(
                f"/cart/learn_course/{course.id}?lesson={first_lesson.id}"
            )
        
        return redirect('cart:learn_course', course.id)

class MyCertificatesView(LoginRequiredMixin, View):

    def get(self, request):
        certificates = Certificate.objects.filter(student=request.user).select_related(
            'course', 'course__instructor__user').order_by('-issued_date')
        context = {
            'certificates': certificates
        }
        return render(request, 'my_certificates.html', context)

class CertificateDetailView(LoginRequiredMixin, View):

    def get(self, request, i):
        certificate = get_object_or_404(Certificate, id=i, student=request.user)
        context = {
            'certificate': certificate,
            'hide_navbar': True,
            'hide_footer': True,
            }
        return render(request, 'certificate_detail.html', context)
    
class DownloadCertificateView(LoginRequiredMixin, View):

    def get(self, request, i):
        certificate = get_object_or_404(Certificate, id=i, student=request.user)

        html = render_to_string("certificate_pdf.html", {"certificate": certificate}, request=request)

        with sync_playwright() as p: #Start Playwright
            browser = p.chromium.launch() #Launch Chromium Browser

            #Creates a new browser tab
            page = browser.new_page(viewport={"width": 1400, "height": 900})

            page.set_content(html, wait_until="networkidle")

            pdf = page.pdf(format="A4", landscape=True, print_background=True, prefer_css_page_size=True,
                margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"})

            browser.close()

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="{certificate.course.title}_Certificate.pdf"'
        )
        return response

