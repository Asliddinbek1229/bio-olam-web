from django.contrib import admin
from .models import Category, Subcategory, Videos, Comments

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'image',
       'subcategory_count',
    ]
    list_filter = [
        'name',
        'image',
       'subcategory_count',
    ]
    search_fields = [
        'name',
        'image',
       'subcategory_count',
    ]
    list_per_page = 10
    list_max_show_all = 100


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = [
        'category',
        'teacher',
        'name',
        'descriptions',
        'image',
        'created_at',
        'student_count',
        'course_duration',
        'videos_count',
    ]


@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'subcategory',
        'time',
        'video',
    ]


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = [
        'video',
        'user',
        'text',
        'created_at',
    ]
    list_filter = [
        'video',
        'text',
        'created_at',
    ]
    search_fields = [
        'video',
        'text',
        'created_at',
    ]
