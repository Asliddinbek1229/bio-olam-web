from django.db import models
from users.models import Teachers

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='category/',
        blank=True,
        null=True
    )
    subcategory_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def update_subcategory_count(self):
        self.subcategory_count = self.subcategories.count()
        self.save()


class Subcategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )
    teacher = models.ForeignKey(
        Teachers,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to="subcategory/",
        blank=True,
        null=True
    )
    student_count = models.IntegerField(default=0)
    course_duration = models.IntegerField(default=0)
    videos_count = models.IntegerField(default=0)

    def update_course_duration(self):
        total_duration = sum(video.time for video in self.videos_set.all())
        self.course_duration = total_duration
        self.save()

    def update_videos_count(self):
        self.videos_count = self.videos_set.count()
        self.save()

    def update_teacher_stats(self):
        self.teacher.courses_num = self.teacher.subcategories.count()
        self.teacher.videos_num = sum(subcategory.videos_set.count() for subcategory in self.teacher.subcategories.all())
        self.teacher.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.category.update_subcategory_count()
        self.update_teacher_stats()

    def delete(self, *args, **kwargs):
        category = self.category
        teacher = self.teacher
        category.update_subcategory_count()
        teacher.update_teacher_stats()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Videos(models.Model):
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    time = models.IntegerField(default=0)
    video = models.FileField(upload_to="videos/")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.subcategory.update_course_duration()
        self.subcategory.update_videos_count()
        self.subcategory.update_teacher_stats()

    def delete(self, *args, **kwargs):
        subcategory = self.subcategory
        super().delete(*args, **kwargs)
        subcategory.update_course_duration()
        subcategory.update_videos_count()
        subcategory.update_teacher_stats()

    def __str__(self):
        return f"{self.subcategory.name} - {self.name}"

