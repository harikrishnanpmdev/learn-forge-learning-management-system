from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from accounts.forms import RegisterForm, LoginForm, CreateCourseForm, SectionForm, LessonForm, QuizForm, QuestionForm, OptionForm
from django.core.mail import send_mail
from accounts.models import CustomUser, Category, Course, Quiz, Question, Option, QuizAttempt, Review, Section, Instructor
from cart.models import Enrollment, Certificate, Lesson, LessonCompletion
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg, Sum

class Categories(View):
    def get(self, request):
        c= Category.objects.all()
        context = {'categories': c}
        return render(request, 'categories.html', context)
    
class Courses(View):
    def get(self, request, i):
        c = Category.objects.get(id=i)
        level = request.GET.get('level')
        courses = c.courses.all()
        if level:
            courses = courses.filter(level=level)
        context = {'category': c, 'course_list': courses, 'selected_level': level}
        return render(request, 'courses.html', context)

class CourseDetail(View):
    def get(self, request, i):
        c= Course.objects.get(id=i)
        context={'course': c}
        return render(request, 'course_detail.html', context)

class AdminHome(View):
    def get(self, request):
        return render(request, 'admin_home.html')
    
class Register(View):
    def get(self, request):
        form_instance = RegisterForm()
        context = {'form': form_instance}
        return render(request, 'register.html', context)
    
    def post(self, request):
        form_instance = RegisterForm(request.POST)
        if form_instance.is_valid():
            f=form_instance.save(commit=False)
            f.is_active = False
            f.save()
            f.generate_otp()

            print("Generated OTP :", f.otp)

            send_mail(
                "OTP Verification - LearnForge",
                f"Your OTP is {f.otp}",
                "harikrishnanpm18@gmail.com",
                [f.email],
                fail_silently=False
            )
        
            return redirect('accounts:otp_verification')
        
        context = {'form': form_instance}
        return render(request, 'register.html', context)

class OTPVerification(View):
    def get(self, request):
        return render(request, 'otp_verification.html')
    
    def post(self, request):
        otp=request.POST['otp']
        try:
            f= CustomUser.objects.get(otp=otp)
            f.is_active = True
            f.is_verified = True
            f.otp = None
            f.save()
            return redirect('accounts:login')
        except CustomUser.DoesNotExist:
            context = {'error': 'Invalid OTP : Please Try Again !'}
            return render(request, 'otp_verification.html', context)

class Login(View):
    def get(self, request):
        form_instance = LoginForm()
        context = {'form': form_instance}
        return render(request, 'login.html', context)
    
    def post(self, request):
        form_instance = LoginForm(request.POST)
        if form_instance.is_valid():
            data = form_instance.cleaned_data
            u = data['username']
            p = data['password']
            user = authenticate(username=u, password=p)
            if user and user.is_superuser == True:
                login(request, user)
                return redirect('accounts:admin_home')#
            elif user and user.want_to_join_as == 'student':
                login(request, user)
                return redirect('accounts:student_dashboard')
            elif user and user.want_to_join_as == 'teacher':
                login(request, user)
                return redirect('accounts:instructor_dashboard')
            else:
                messages.error(request, 'Invalid Credentials : Please Try Again !')
                return redirect('accounts:login')

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')

class QuizView(LoginRequiredMixin, View):
    def get(self, request, i):
        course = get_object_or_404(Course, id=i)
        enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
        
        if not enrolled:
            messages.error(request, "You are not enrolled in this course.")
            return redirect('accounts:coursedetails',i)
        
        quiz = get_object_or_404(Quiz, course=course, is_active=True)
        questions = Question.objects.filter(quiz=quiz).prefetch_related('options')
        context = {'course': course, 'quiz': quiz, 'questions': questions}
        return render(request, 'quiz.html', context)

class SubmitQuizView(LoginRequiredMixin, View):
    def post(self, request, i):
        quiz = get_object_or_404(Quiz, id=i, is_active=True)
        questions = Question.objects.filter(quiz=quiz).prefetch_related('options')
        total_questions = questions.count()
        score = 0

        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option:
                correct_option = question.options.filter(is_correct=True).first()

                if (correct_option and str(correct_option.id) == selected_option):
                    score += 1
        
        percentage = 0
        if total_questions > 0:
            percentage = round((score / total_questions) * 100, 2)
        
        is_passed = percentage >= quiz.pass_percentage
        attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            is_passed=is_passed
        )
        return redirect('accounts:quiz_result', attempt.id)
    
class QuizResultView(LoginRequiredMixin, View):
    def get(self, request, i):
        attempt = get_object_or_404(QuizAttempt, id=i, student=request.user)
        certificate = None
        if attempt.is_passed:
            certificate, created = Certificate.objects.get_or_create(
                student=request.user,
                course=attempt.quiz.course
            )

        context = {
            "attempt": attempt,
            "quiz": attempt.quiz,
            "course": attempt.quiz.course,
            "certificate": certificate
        }
        return render(request, "quiz_result.html", context)

class StudentDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        purchased_courses = Enrollment.objects.filter(student=request.user).select_related("course")
        total_courses = purchased_courses.count()
        completed_courses = 0
        certificates = Certificate.objects.filter(student=request.user)
        certificate_count = certificates.count()
        quiz_attempts = QuizAttempt.objects.filter(student=request.user, is_passed=True)
        average_score = 0

        if quiz_attempts.exists():
            average_score = round(quiz_attempts.aggregate(Avg("percentage"))["percentage__avg"],1)
        
        for enrollment in purchased_courses:
            total_lessons = Lesson.objects.filter(section__course=enrollment.course).count()

            completed_lessons = LessonCompletion.objects.filter(student=request.user, lesson__section__course=enrollment.course).count()

            if total_lessons > 0:
                enrollment.progress_percentage = round((completed_lessons / total_lessons) * 100)
            else:
                enrollment.progress_percentage = 0

            if (total_lessons > 0 and total_lessons == completed_lessons):
                completed_courses += 1
        
        context = {
            "total_courses": total_courses,
            "completed_courses": completed_courses,
            "certificate_count": certificate_count,
            "average_score": average_score,
            "purchased_courses": purchased_courses,
            "certificates": certificates[:3],
        }
        return render(request, "student_dashboard.html", context)

class InstructorDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        instructor = request.user.instructor
        courses = Course.objects.filter(instructor=instructor).prefetch_related("reviews","quizzes")
        total_courses = courses.count()

        total_students = courses.aggregate(total=Sum("students"))["total"] or 0

        average_rating = courses.aggregate(avg=Avg("rating"))["avg"] or 0

        total_quizzes = Quiz.objects.filter(course__instructor=instructor).count()

        recent_courses = courses.order_by("-created_at")[:3]

        recent_reviews = Review.objects.filter(course__instructor=instructor).select_related("user","course").order_by("-created_at")[:3]

        context = {
            "instructor": instructor,
            "total_courses": total_courses,
            "total_students": total_students,
            "average_rating": round(average_rating,1),
            "total_quizzes": total_quizzes,
            "recent_courses": recent_courses,
            "recent_reviews": recent_reviews,
        }
        return render(request, "instructor_dashboard.html", context)

class CreateCourseView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.want_to_join_as != "teacher":
            messages.error(request, "Only Instructors can Create Courses.")
            return redirect("accounts:categories")
        form = CreateCourseForm()
        return render(request, "create_course.html", {"form": form})
    
    def post(self, request):
        if request.user.want_to_join_as != "teacher":
            messages.error(request, "Only Instructors can Create Courses.")
            return redirect("accounts:categories")
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user.instructor
            course.save()
            form.save_m2m()
            messages.success(request, "Course Created Successfully.")
            return redirect("accounts:my_courses")
        return render(request, "create_course.html", {"form": form})

class MyCoursesView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.want_to_join_as != "teacher":
            messages.error(request, "Access denied.")
            return redirect("accounts:categories")
        
        instructor = request.user.instructor
        courses = Course.objects.filter(instructor=instructor).select_related("category").order_by("-created_at")
        total_students = courses.aggregate(total=Sum("students"))["total"] or 0
        total_lessons = courses.aggregate(total=Sum("lessons"))["total"] or 0
        average_rating = courses.aggregate(avg=Avg("rating"))["avg"] or 0

        context = {"courses": courses, "total_students": total_students, "total_lessons": total_lessons, "average_rating": round(average_rating,1)}
        return render(request, "instructor_courses.html", context)

class EditCourseView(LoginRequiredMixin, View):
    def get(self, request, i):
        if request.user.want_to_join_as != "teacher":
            messages.error(request, "Access denied.")
            return redirect("accounts:categories")

        course = get_object_or_404(Course, id=i, instructor=request.user.instructor)
        form = CreateCourseForm(instance=course)
        return render(request, "edit_course.html", {"form": form, "course": course})

    def post(self, request, i):
        if request.user.want_to_join_as != "teacher":
            messages.error(request, "Access denied.")
            return redirect("accounts:categories")

        course = get_object_or_404(Course, id=i, instructor=request.user.instructor)
        form = CreateCourseForm(request.POST, instance=course)

        if form.is_valid():
            updated_course = form.save(commit=False)
            updated_course.instructor = request.user.instructor
            updated_course.save()
            form.save_m2m()
            messages.success(request, "Course Updated Successfully.")
            return redirect("accounts:my_courses")
        return render(request, "edit_course.html", {"form": form, "course": course})
    
class ManageCurriculumView(LoginRequiredMixin, View):
    def get(self, request, i):
        if request.user.want_to_join_as != "teacher":
            messages.error(request, "Access denied.")
            return redirect("accounts:categories")

        course = get_object_or_404(Course, id=i, instructor=request.user.instructor)
        sections = Section.objects.filter(course=course).order_by("id")
        form = SectionForm()
        context = {"course": course, "sections": sections, "form": form}
        return render(request, "manage_curriculum.html", context)
    
class AddChapterView(LoginRequiredMixin, View):
    def post(self, request, i):
        if request.user.want_to_join_as != "teacher":
            messages.error(request, "Access denied.")
            return redirect("accounts:categories")

        course = get_object_or_404(Course, id=i, instructor=request.user.instructor)
        form = SectionForm(request.POST)

        if form.is_valid():
            section = form.save(commit=False)
            section.course = course
            section.save()
            messages.success(request, "Chapter Added Successfully")
        else:
            messages.error(request, "Please Enter a Valid Chapter Name")

        return redirect("accounts:manage_curriculum", i=course.id)

class EditChapterView(LoginRequiredMixin, View):
    def post(self, request, i):
        section = get_object_or_404(Section, id=i, course__instructor=request.user.instructor)
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            messages.success(request, "Chapter Updated Successfully")
        else:
            messages.error(request, "Please Enter a valid Chapter Name")
        return redirect("accounts:manage_curriculum",i=section.course.id)

class DeleteChapterView(LoginRequiredMixin, View):
    def post(self, request, i):
        section = get_object_or_404(Section, id=i, course__instructor=request.user.instructor)
        course_id = section.course.id
        chapter_name = section.chapter
        section.delete()
        messages.success(request, f'"{chapter_name}" Deleted Successfully')
        return redirect("accounts:manage_curriculum", i=course_id)

class ManageLessonsView(LoginRequiredMixin, View):
    def get(self, request, i):
        section = get_object_or_404(Section, id=i, course__instructor=request.user.instructor)
        lessons = Lesson.objects.filter(section=section).order_by("lesson_order")
        form = LessonForm()
        context = {"section": section, "course": section.course, "lessons": lessons, "form": form}
        return render(request, "manage_lessons.html", context)

class AddLessonView(LoginRequiredMixin, View):
    def post(self, request, i):
        section = get_object_or_404(Section, id=i, course__instructor=request.user.instructor)
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.section = section
            lesson.save()
            messages.success(request, "Lesson Added Successfully")
        else:
            messages.error(request, "Please Correct the Errors and Try Again")
        return redirect("accounts:manage_lessons", i=section.id)

class EditLessonView(LoginRequiredMixin, View):
    def post(self, request, i):
        lesson = get_object_or_404(Lesson, id=i)
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect("accounts:manage_lessons", i=lesson.section.id)
        return redirect("accounts:manage_lessons", i=lesson.section.id)

class DeleteLessonView(LoginRequiredMixin, View):
    def post(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        lesson = get_object_or_404(Lesson, id=i, section__course__instructor=instructor)
        section_id = lesson.section_id
        lesson.delete()
        messages.success(request, "Lesson Deleted Successfully")
        return redirect("accounts:manage_lessons", i=section_id)

class DeleteCourseView(LoginRequiredMixin, View):
    def post(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        course = get_object_or_404(Course, id=i, instructor=instructor)
        course.delete()
        messages.success(request, "Course Deleted Successfully")
        return redirect("accounts:my_courses")

class ManageQuizView(LoginRequiredMixin, View):
    def get(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        course = get_object_or_404(Course, id=i, instructor=instructor)
        quizzes = Quiz.objects.filter(course=course)
        context = {"course": course, "quizzes": quizzes}
        return render(request, "manage_quiz.html", context)

class CreateQuizView(LoginRequiredMixin, View):
    def get(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        course = get_object_or_404(Course, id=i, instructor=instructor)
        form = QuizForm()
        context = {"course": course, "form": form}
        return render(request, "create_quiz.html", context)

    def post(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        course = get_object_or_404(Course, id=i, instructor=instructor)
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.success(request, "Quiz Created Successfully")
            return redirect("accounts:manage_quiz", i=course.id)
        context = {"course": course, "form": form}
        return render(request, "create_quiz.html", context)

class EditQuizView(LoginRequiredMixin, View):
    def get(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        quiz = get_object_or_404(Quiz, id=i, course__instructor=instructor)
        form = QuizForm(instance=quiz)
        context = {"quiz": quiz, "course": quiz.course, "form": form}
        return render(request, "edit_quiz.html", context)

    def post(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        quiz = get_object_or_404(Quiz, id=i, course__instructor=instructor)
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, "Quiz Updated Successfully")
            return redirect("accounts:manage_quiz", i=quiz.course.id)
        context = {"quiz": quiz, "course": quiz.course, "form": form}
        return render(request, "edit_quiz.html", context)

class AddQuestionView(LoginRequiredMixin, View):
    def get(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        quiz = get_object_or_404(Quiz, id=i, course__instructor=instructor)
        form = QuestionForm()
        context = {"quiz": quiz, "course": quiz.course, "form": form}
        return render(request, "add_question.html", context)

    def post(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        quiz = get_object_or_404(Quiz, id=i, course__instructor=instructor)
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, "Question Added Successfully")
            return redirect("accounts:manage_questions", i=quiz.id)
        context = {"quiz": quiz, "course": quiz.course, "form": form}
        return render(request, "add_question.html", context)

class ManageQuestionsView(LoginRequiredMixin, View):
    def get(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        quiz = get_object_or_404(Quiz, id=i, course__instructor=instructor)
        questions = Question.objects.filter(quiz=quiz).order_by("question_order")
        context = {"quiz": quiz, "course": quiz.course, "questions": questions,}
        return render(request, "manage_questions.html", context)

class ManageOptionsView(LoginRequiredMixin, View):
    def get(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        question = get_object_or_404(Question, id=i, quiz__course__instructor=instructor)
        options = Option.objects.filter(question=question)
        form = OptionForm()
        context = {"question": question, "quiz": question.quiz, "course": question.quiz.course, "options": options, "form": form}
        return render(request, "manage_options.html", context)

    def post(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        question = get_object_or_404(Question, id=i, quiz__course__instructor=instructor)
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question = question
            if option.is_correct:
                Option.objects.filter(question=question).update(is_correct=False)
            option.save()
            messages.success(request, "Option Added Successfully")
            return redirect("accounts:manage_options", i=question.id)
        options = Option.objects.filter(question=question)
        context = {
            "question": question, "quiz": question.quiz, "course": question.quiz.course,
            "options": options, "form": form
        }
        return render(request, "manage_options.html", context)

class EditOptionView(LoginRequiredMixin, View):
    def get(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        option = get_object_or_404(Option, id=i, question__quiz__course__instructor=instructor)
        form = OptionForm(instance=option)
        context = {
            "option": option, "question": option.question, "quiz": option.question.quiz,
            "course": option.question.quiz.course, "form": form,
        }
        return render(request, "edit_option.html", context)

    def post(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        option = get_object_or_404(Option, id=i, question__quiz__course__instructor=instructor)
        form = OptionForm(request.POST, instance=option)
        if form.is_valid():
            updated_option = form.save(commit=False)
            if updated_option.is_correct:
                Option.objects.filter(question=option.question).exclude(id=option.id).update(is_correct=False)
            updated_option.save()
            messages.success(request, "Option Updated Successfully")
            return redirect("accounts:manage_options", i=option.question.id)
        context = {
            "option": option, "question": option.question, "quiz": option.question.quiz,
            "course": option.question.quiz.course, "form": form,
        }
        return render(request, "edit_option.html", context)

class DeleteOptionView(LoginRequiredMixin, View):
    def post(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        option = get_object_or_404(Option, id=i, question__quiz__course__instructor=instructor)
        question_id = option.question.id
        option.delete()
        messages.success(request, "Option Deleted Successfully")
        return redirect("accounts:manage_options", i=question_id)

class EditQuestionView(LoginRequiredMixin, View):
    def get(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        question = get_object_or_404(Question, id=i, quiz__course__instructor=instructor)
        form = QuestionForm(instance=question)
        context = {
            "question": question, "quiz": question.quiz,
            "course": question.quiz.course, "form": form,
        }
        return render(request, "edit_question.html", context)

    def post(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        question = get_object_or_404(Question, id=i, quiz__course__instructor=instructor)
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question Updated Successfully")
            return redirect("accounts:manage_questions", i=question.quiz.id)
        context = {
            "question": question, "quiz": question.quiz,
            "course": question.quiz.course, "form": form,
        }
        return render(request, "edit_question.html", context)

class DeleteQuestionView(LoginRequiredMixin, View):
    def post(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        question = get_object_or_404(Question, id=i, quiz__course__instructor=instructor)
        quiz_id = question.quiz.id
        question.delete()
        messages.success(request, "Question Deleted Successfully")
        return redirect("accounts:manage_questions", i=quiz_id)

class DeleteQuizView(LoginRequiredMixin, View):
    def post(self, request, i):
        instructor = get_object_or_404(Instructor, user=request.user)
        quiz = get_object_or_404(Quiz, id=i, course__instructor=instructor)
        course_id = quiz.course.id
        quiz.delete()
        messages.success(request, "Quiz Deleted Successfully")
        return redirect("accounts:manage_quiz", i=course_id)

