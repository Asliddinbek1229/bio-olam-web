from django.contrib import admin
from .models import Profile, Teachers

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'photo',
        'date_of_birth',
        'job',
        'bio',
    ]

@admin.register(Teachers)
class TeachersAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'teacher_type',
        'bio',
        'likes_num',
        'student_num',
    ]