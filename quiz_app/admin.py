from django.contrib import admin

# Register your models here.
from .models import Quiz

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'date',
        'topic',
        'number_of_questions',
        'time',
        'required_score',
        'difficulty',
    ]
    list_filter = [
        'name',
        'date',
        'topic',
        'number_of_questions',
    ]
    search_fields = [
        'name',
        'date',
        'topic',
        'number_of_questions',
    ]
    ordering = [
        '-date',
    ]
