from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser, Course, Section, Quiz, Question, Option
from django import forms
from cart.models import Lesson

class RegisterForm(UserCreationForm):
    
    role_choices = [('student', 'Student'),('teacher', 'Teacher')]

    want_to_join_as = forms.ChoiceField(choices=role_choices)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'want_to_join_as', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)

class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ["instructor", "rating", "rating_no", "students", "lessons", "created_at", "updated_at",]
        
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),

            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Course Title"}),

            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Short Course Description"}),

            "course_description": forms.Textarea(attrs={"class": "form-control", "rows": 6, "placeholder": "Detailed Course Description"}),

            "duration": forms.TextInput(attrs={"class": "form-control", "placeholder": "Example: 35h"}),

            "old_price": forms.NumberInput(attrs={"class": "form-control"}),

            "price": forms.NumberInput(attrs={"class": "form-control"}),

            "tags": forms.SelectMultiple(attrs={"class": "form-select"}),

            "bg1": forms.TextInput(attrs={"class": "form-control", "type": "color"}),

            "bg2": forms.TextInput(attrs={"class": "form-control", "type": "color"}),

            "icon": forms.TextInput(attrs={"class": "form-control", "placeholder": "Example: bi bi-laptop"}),

            "level": forms.Select(attrs={"class": "form-select"}),

            "language": forms.Select(attrs={"class": "form-select"}),
        }

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["chapter"]

        widgets = {
            "chapter": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter chapter name"}),
        }

        labels = {
            "chapter": "Chapter Name "
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "description", "video", "thumbnail", "duration", "lesson_order", "is_preview"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter lesson title"}),

            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter lesson description", "rows": 4}),

            "video": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "video/*"}),

            "thumbnail": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),

            "duration": forms.TextInput(attrs={"class": "form-control", "placeholder": "Example: 10 mins"}),

            "lesson_order": forms.NumberInput(attrs={"class": "form-control", "min": 1}),

            "is_preview": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

        labels = {"title": "Lesson Title ", "description": "Description ", "video": "Lesson Video ",
            "thumbnail": "Lesson Thumbnail ", "duration": "Duration ", "lesson_order": "Lesson Order ", "is_preview": "Allow Free Preview",
        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["title", "description", "time_limit", "pass_percentage", "is_active"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter quiz title"}),

            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Enter quiz description"}),

            "time_limit": forms.NumberInput(attrs={"class": "form-control", "min": 1}),

            "pass_percentage": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 100}),

            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"})
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question", "question_order"]

        widgets = {
            "question": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Enter the question"}),
            "question_order": forms.NumberInput(attrs={"class": "form-control", "min": 1, "placeholder": "Example: 1"}),
        }

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["option_text", "is_correct"]

        widgets = {
            "option_text": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter answer option"}),
            "is_correct": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
