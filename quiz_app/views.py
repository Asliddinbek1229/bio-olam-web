from django.views.generic import DetailView
from django.http import JsonResponse
from results.models import Result
from questions.models import Question, Answer
from .models import Quiz
from users.models import Profile
from django.shortcuts import render, get_object_or_404

class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/detail.html'


def quiz_detail_view(request, id):
    quiz = get_object_or_404(Quiz, pk=id)
    context = {
        'quiz': quiz
    }
    return render(request, 'quiz/detail.html', context)


def quiz_detail_data_view(request, id):
    quiz = Quiz.objects.get(id=id)
    questions = []
    for question in quiz.get_questions:
        print(quiz.get_questions)
        answers = []
        for answer in question.get_answers:
            answers.append(answer.text)
        questions.append({question.text: answers})
    
    return JsonResponse({
        'data': questions,
        'time': quiz.time
    })


def save_quiz_view(request, id):
    if request.accepts("application/json"):
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')

        questions = []

        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)

        profile = Profile.objects.get(user=request.user)
        quiz = Quiz.objects.get(id=id)

        required_score = quiz.required_score
        score = 0
        multiplier = 100 / len(questions) 
        results = []

        for q in questions:
            a_selected = data[q.text]

            if a_selected != '':
                correct_answer = Answer.objects.filter(question=q).get(correct=True)
                if a_selected == correct_answer.text:
                    score += 1
                
                results.append({q.text: {
                    'correct_answer': correct_answer.text,
                    'answered': a_selected
                }})
            else:
                results.append({q.text: 'not answered'})

        final_score = score * multiplier


        Result.objects.create(quiz=quiz, user=profile, score=final_score)

        json_response = {
            'score': final_score,
            'correct_questions': score,
            'passed': False,
            'required_score': required_score,
            'results': results
        }

        if final_score >= required_score:
            json_response['passed'] = True
            return JsonResponse(json_response)    

        return JsonResponse(json_response)