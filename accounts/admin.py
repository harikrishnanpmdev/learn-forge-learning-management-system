from django.contrib import admin
from accounts.models import CustomUser, Category, Instructor, Course, LearnPoint, Requirement
from accounts.models import Tag, Section, ChapterTopics, Review, Quiz, Question, Option, QuizAttempt

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(LearnPoint)
admin.site.register(Requirement)
admin.site.register(Tag)
admin.site.register(Section)
admin.site.register(ChapterTopics)
admin.site.register(Review)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(QuizAttempt)

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self,db_field,request,**kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = CustomUser.objects.filter(want_to_join_as="teacher")
        return super().formfield_for_foreignkey(db_field,request,**kwargs)
