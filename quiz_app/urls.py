from django.urls import path
from .views import QuizListView, QuizDetailView, quiz_detail_data_view, save_quiz_view

urlpatterns = [
    path('quizzes/<int:subcategory_id>/', QuizListView.as_view(), name='quiz-list'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quiz/<int:pk>/data/', quiz_detail_data_view, name='quiz-data'),
    path('quiz/<int:pk>/save/', save_quiz_view, name='quiz-save'),
]
