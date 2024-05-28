from django.contrib import admin
from .models import Category, Subcategory, Videos

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
        'id',
        'category',
        'name',
        'image',
        'videos_count',
        'course_duration',
        'student_count',
    ]


@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'subcategory',
        'time',
        'video',
    ]



