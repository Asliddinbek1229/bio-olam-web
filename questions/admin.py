from django.contrib import admin

from .models import Question, Answer

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = [
        'quiz',
        'date',
    ]
    list_filter = [
        'quiz',
        'date',
    ]
    search_fields = [
        'quiz',
        'date',
    ]
    ordering = [
        '-date',
    ]



admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)