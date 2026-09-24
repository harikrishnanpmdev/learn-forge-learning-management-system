from django.urls import path
from cart import views

app_name = 'cart'

urlpatterns = [
    path('addtocart/<int:i>', views.AddToCart.as_view(), name='addtocart'),
    path('cartview', views.CartView.as_view(), name='cartview'),
    path('removefromcart/<int:i>', views.RemoveFromCart.as_view(), name='removefromcart'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('payment_success', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('my_courses', views.MyCoursesView.as_view(), name='my_courses'),
    path('learn_course/<int:i>', views.CourseLearningView.as_view(), name='learn_course'),
    path('complete_lesson/<int:i>/', views.CompleteLessonView.as_view(), name='complete_lesson'),
    path('resume_course/<int:i>/', views.ResumeLearningView.as_view(), name='resume_course'),
    path('my_certificates', views.MyCertificatesView.as_view(), name='my_certificates'),
    path('certificate/<int:i>/', views.CertificateDetailView.as_view(), name='certificate_detail'),
    path('download_certificate/<int:i>/', views.DownloadCertificateView.as_view(), name='download_certificate'),
]
