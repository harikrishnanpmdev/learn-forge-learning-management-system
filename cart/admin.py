from django.contrib import admin
from cart.models import Cart, Order, OrderItem, Enrollment, Lesson, LessonCompletion, Certificate

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Enrollment)
admin.site.register(Lesson)
admin.site.register(LessonCompletion)
admin.site.register(Certificate)