from django import forms
from questions.models import Quiz, Question, Answer
from courses.models import Subcategory

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'description', 'subcategory', 'number_of_questions', 'time', 'required_score', 'difficulty']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Foydalanuvchini init orqali qabul qilamiz
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subcategory'].queryset = Subcategory.objects.filter(teacher=user.teacher)


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.teacher = kwargs.pop('teacher', None)
        super(QuestionForm, self).__init__(*args, **kwargs)

        # Agar teacher foydalanuvchi bo'lsa, uning quizlarini filterlaymiz
        if self.teacher:
            self.fields['quiz'].queryset = Quiz.objects.filter(teacher=self.teacher)

    class Meta:
        model = Question
        fields = ['text', 'quiz']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'correct']  # 'question' maydoni foydalanuvchiga ko'rsatilmaydi

