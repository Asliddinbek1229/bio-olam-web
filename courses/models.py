from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    class CourseType(models.TextChoices):
        Free = "Free", "Free"
        Paid = "Paid", "Paid"
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )
    teacher = models.ForeignKey(
        'users.Teachers',
        on_delete=models.CASCADE,
        related_name='subcategories'
    )
    course_type = models.CharField(
        max_length=200,
        choices=CourseType.choices,
        default=CourseType.Free
    )
    name = models.CharField(max_length=100)
    descriptions = models.TextField()
    image = models.ImageField(
        upload_to="subcategory/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    student_count = models.IntegerField(default=0)
    course_duration = models.IntegerField(default=0)
    videos_count = models.IntegerField(default=0)
    is_payment = models.BooleanField(default=False)
    old_price = models.IntegerField(default=0)
    price = models.BigIntegerField(default=0)
    purchased_count = models.IntegerField(default=0)

    def increment_purchased_count(self):
        self.purchased_count += 1
        self.save()
        print(f"{self.name} xarid qilinganlar soni yangilandi: {self.purchased_count}")

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
        super().delete(*args, **kwargs)
        category.update_subcategory_count()
        teacher.update_teacher_stats()

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Videos(models.Model):
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    time = models.IntegerField(default=0, null=False, blank=False)
    video = models.FileField(upload_to="videos/")
    likes_num = models.ManyToManyField(User, related_name="videos_like", blank=True)
    comment_num = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    cover_image = models.ImageField(upload_to="videos/covers/", default="static/images/post-1-1.png")

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

    def number_of_likes(self):
        return self.likes_num.count()

    def increment_comments(self):
        self.comment_num += 1
        self.save()

    def __str__(self):
        return f"{self.subcategory.name} - {self.name}"



class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'video']

    def __str__(self):
        return f"{self.user.username} likes {self.video.name}"


class Comments(models.Model):
    video = models.ForeignKey(
        Videos,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.video.name} - {self.text}"