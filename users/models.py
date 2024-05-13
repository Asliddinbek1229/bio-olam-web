from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class CustomUser(AbstractUser):
#     class JobStatus(models.TextChoices):
#         Student = "STUDENT", "O'quvchi"
#         Teacher = "TEACHER", "O'qituvchi"
#         Other = "OTHER", "Boshqa"
    
#     date_of_birth = models.DateField(blank=True, null=True)
#     image = models.ImageField(upload_to='users/', blank=True, null=True)
#     job = models.CharField(
#         max_length=10,
#         choices=JobStatus.choices,
#         default=JobStatus.Other
#     )

#     def __str__(self) -> str:
#         return f"{self.job}"
