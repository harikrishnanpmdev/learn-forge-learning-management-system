from django.db import models
from django.contrib.auth.models import AbstractUser
import random

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    want_to_join_as = models.CharField(max_length=20, blank=True)
    icon = models.CharField(max_length=5, blank=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=10, null=True, blank=True)

    def save(self, *args, **kwargs):
        first_name = ""
        last_name = ""

        if self.first_name:
            first_name = self.first_name[:1].upper()

        if self.last_name:
            last_name = self.last_name[:1].upper()

        self.icon = first_name + last_name
        super().save(*args, **kwargs)

    def generate_otp(self):
        otp = str(random.randint(1000, 9999)) + str(self.id)
        self.otp = otp
        self.save()
    
    def __str__(self):
        return self.username
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to="category")

    def __str__(self):
        return self.name
    
class Instructor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="instructor")
    background_color = models.CharField(max_length=20, default="#5046e5")
    bio = models.TextField()
    designation = models.CharField(max_length=200)
    skill_1 = models.CharField(max_length=100)
    skill_2 = models.CharField(max_length=100)
    skill_3 = models.CharField(max_length=100)
    experience = models.CharField(max_length=200)
    students = models.IntegerField(default=0)
    courses = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Course(models.Model):

    LEVEL_CHOICES = (
        ('Best Seller', 'Best Seller'),
        ('New', 'New'),
        ('Trending', 'Trending'),
        ('Popular', 'Popular'),
    )

    LANGUAGE_CHOICES = (
        ('English', 'English'),
        ('Malayalam', 'Malayalam'),
        ('Hindi', 'Hindi'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses_list')
    title = models.CharField(max_length=250)
    description = models.TextField()
    course_description = models.TextField(blank=True,null=True)
    rating = models.FloatField(default=0)
    rating_no = models.IntegerField(default=0)
    duration = models.CharField(max_length=50)
    lessons = models.IntegerField(default=0)
    students = models.IntegerField(default=0)
    old_price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    tags = models.ManyToManyField('Tag', related_name='courses')
    bg1 = models.CharField(max_length=20, default="#5046e5")
    bg2 = models.CharField(max_length=20, default="#7c3aed")
    icon = models.CharField(max_length=100)
    level = models.CharField(max_length=50,choices=LEVEL_CHOICES,default='Best Seller')
    language = models.CharField(max_length=50,choices=LANGUAGE_CHOICES,default='English')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
    
class LearnPoint(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='learn_points')
    point = models.CharField(max_length=300)

    def __str__(self):
        return self.course.title
    
class Requirement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='requirements')
    requirement = models.CharField(max_length=300)

    def __str__(self):
        return self.course.title
    
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    chapter = models.CharField(max_length=200)

    def __str__(self):
        return self.chapter
    
class ChapterTopics(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='points')
    topic = models.CharField(max_length=300)

    def __str__(self):
        return self.topic
    
class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=5)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    time_limit = models.PositiveIntegerField(default=30)
    pass_percentage = models.PositiveIntegerField(default=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    question_order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['question_order']
    
    def __str__(self):
        return self.question[:60]
    
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text

class QuizAttempt(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_passed = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-attempted_at']
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.quiz.title}"

