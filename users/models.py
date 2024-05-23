from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    class Jobs(models.TextChoices):
        Other = "Other", "Other"
        Student = "STDT", "Student"
        Teacher = "TEACH", "Teacher"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
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
    bio = models.CharField(max_length=200)

    
    def __str__(self):
        return f"{self.user.username} profili"