from django.urls import path
from . import views

urlpatterns = [
    path('quiz/create/', views.create_quiz_view, name='create-quiz'),
    path('question/create/', views.create_question_and_answers_view, name='create-question-answer'),
    path('quiz/<int:quiz_id>/edit/', views.edit_quiz_view, name='edit_quiz'),
    path('question/<int:id>/edit/', views.edit_question_and_answers_view, name='edit_question_and_answers'),
]