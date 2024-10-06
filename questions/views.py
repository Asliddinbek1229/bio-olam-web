from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory

from quiz_app.models import Quiz
from .models import Question, Answer
from .forms import QuizForm, QuestionForm, AnswerForm

# Create your views here.
def create_quiz_view(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_page')  # Quizlar ro'yxatiga qaytish
    else:
        form = QuizForm()
    return render(request, 'quiz/create_quiz.html', {'form': form})

def create_question_and_answers_view(request):
    AnswerFormSet = formset_factory(AnswerForm, extra=4)  # 4 ta Answer kiritish uchun formset yaratamiz

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        answer_formset = AnswerFormSet(request.POST)

        if question_form.is_valid() and answer_formset.is_valid():
            question = question_form.save()  # Savolni saqlaymiz

            for answer_form in answer_formset:
                answer = answer_form.save(commit=False)
                answer.question = question  # Har bir Answer'ni ushbu savolga bog'laymiz
                answer.save()

            return redirect('home_page')  # Muvaffaqiyatli yaratgandan so'ng redirect qilamiz
    else:
        question_form = QuestionForm()
        answer_formset = AnswerFormSet()

    return render(request, 'quiz/create_question_and_answers.html', {
        'question_form': question_form,
        'answer_formset': answer_formset,
    })


# Viktorina tahrirlash view
def edit_quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz_list')  # Viktorina ro'yxatiga qaytish
    else:
        form = QuizForm(instance=quiz)

    return render(request, 'quiz/edit_quiz.html', {'form': form, 'quiz': quiz})


# Savol va javoblarni tahrirlash view
def edit_question_and_answers_view(request, id):
    question = get_object_or_404(Question, id=id)
    AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=0)  # Yangi javoblar qo'shmaslik uchun extra=0

    if request.method == 'POST':
        question_form = QuestionForm(request.POST, instance=question)
        answer_formset = AnswerFormSet(request.POST, queryset=Answer.objects.filter(question=question))

        if question_form.is_valid() and answer_formset.is_valid():
            question_form.save()

            for answer_form in answer_formset:
                answer_form.save()

            return redirect('quiz_list')  # Muvaffaqiyatli yaratgandan so'ng redirect qilamiz
    else:
        question_form = QuestionForm(instance=question)
        answer_formset = AnswerFormSet(queryset=Answer.objects.filter(question=question))

    return render(request, 'quiz/edit_question_and_answers.html', {
        'question_form': question_form,
        'answer_formset': answer_formset,
        'question': question,
    })