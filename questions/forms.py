from django import forms
from questions.models import Quiz, Question, Answer

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'description', 'topic', 'number_of_questions', 'time', 'required_score', 'difficulty']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'quiz']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'correct']  # 'question' maydoni foydalanuvchiga ko'rsatilmaydi

