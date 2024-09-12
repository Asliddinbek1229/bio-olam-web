from django.contrib import admin
from .models import Profile, Teachers, Review, PurchasedPlaylist

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

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'review_text',
        'rating',
        'created_at',
    ]

@admin.register(PurchasedPlaylist)
class PurchasedPlaylistAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'subcategory',
        'purchased_at',
    ]