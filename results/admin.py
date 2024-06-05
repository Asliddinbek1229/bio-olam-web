from django.contrib import admin
from .models import Result

# Register your models here.
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'quiz',
        'user',
       'score',
    ]
    list_filter = [
        'date',
        'quiz',
        'user',
       'score',
    ]
    ordering = [
        '-date',
    ]