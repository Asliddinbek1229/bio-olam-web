from django.db import models
from django.contrib.auth.models import User
from courses.models import Subcategory

class Profile(models.Model):
    class Jobs(models.TextChoices):
        Other = "Other", "Other"
        Student = "Student", "Student"
        Teacher = "Teacher", "Teacher"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    photo = models.ImageField(
        upload_to='users/',
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True
    )
    job = models.CharField(
        max_length=50,
        choices=Jobs.choices,
        default=Jobs.Other
    )
    saved_playlists = models.ManyToManyField(Subcategory, related_name='saved_by_users', blank=True)
    bio = models.CharField(max_length=200)
    liked_videos_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)

    
    def __str__(self):
        return f"{self.user.username} profili"
    
class Teachers(models.Model):
    class TeacherType(models.TextChoices):
        Other = "Other", "Other"
        Biology = "Biologiya", "Biology"
        Chemistry = "Kimyo", "Chemistry"
        Physics = "Physics", "Physics"
        Math = "Matematika", "Math"
        English = "Ingliz tili", "English"
        History = "Tarix", "History"
        Geography = "Geografiya", "Geography"
        ComputerScience = "Computer Science", "Computer Science"
        Literature = "Adabiyot", "Literature"
        Art = "San'at", "Art"
        Music = "Musiqa", "Music"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher'
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='user_teachers',
    )
    teacher_type = models.CharField(
        max_length=200,
        choices=TeacherType.choices,
        default=TeacherType.Other
    )
    bio = models.TextField()
    courses_num = models.IntegerField(default=0)
    videos_num = models.IntegerField(default=0)
    student_num = models.IntegerField(default=0)
    likes_num = models.IntegerField(default=0)
    comments_num = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.teacher_type}"
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        help_text="0 dan 5 gacha baho bering"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating} stars"