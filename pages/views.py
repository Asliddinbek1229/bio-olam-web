from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from courses.models import Category, Subcategory, Videos, Likes, Comments
from django.contrib.auth.models import User
from users.models import Teachers
from .forms import CommentForm
from courses.models import Comments
from quiz_app.models import Quiz
from results.models import Result
from django.views.generic import ListView
from django.db.models import Q

from users.forms import ReviewForm
from users.models import Review


# Create your views here.
def home_page(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all().order_by('-created_at')[:6]

    total_likes = sum(video.likes_num.count() for video in Videos.objects.all())
    total_comments = Comments.objects.count()

    context = {
        'categories': categories,
        'subcategories': subcategories,
        'total_likes': total_likes,
        'total_comments': total_comments
    }
    return render(request, 'home.html', context)

def about_page(request):
    subcategory_count = Subcategory.objects.count
    users_count = User.objects.count
    teachers_count = Teachers.objects.count
    reviews = Review.objects.all().order_by('-created_at')[:6]
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('about_page')
    else:
        form = ReviewForm()
    
    context = {
       'subcategory_count': subcategory_count,
        'users_count': users_count,
        'teachers_count': teachers_count,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'side_bar/about.html', context)


def contact_me_view(request):
    return render(request, 'side_bar/contact.html')


def tutor_contact_view(request):
    return render(request, 'pages/tutor_contact.html')

def courses_view(request):
    courses = Subcategory.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'side_bar/courses.html', context)


def category_detail_view(request, id):
    category = get_object_or_404(Category, id=id)
    subcategories = Subcategory.objects.all().filter(category=category)
    context = {
        'category': category,
        'subcategories': subcategories
    }
    return render(request, 'pages/category_detail.html', context)

def playlists_view(request, id):
    subcategory = get_object_or_404(Subcategory.objects.all(), id=id)
    quizzes = Quiz.objects.filter(topic=subcategory)
    profile = request.user.profile

    if request.method == 'POST':
        if profile.saved_playlists.filter(id=subcategory.id).exists():
            profile.saved_playlists.remove(subcategory)
        else:
            profile.saved_playlists.add(subcategory)
        return redirect('playlists_view', id=id)
    
    videos = subcategory.videos_set.all()
    quiz_results = {}
    for quiz in quizzes:
        latest_result = Result.objects.filter(user=profile, quiz=quiz).order_by('-date').first()
        quiz_results[quiz.pk] = latest_result

    context = {
        'subcategory': subcategory,
        'videos': videos,
         'is_saved': profile.saved_playlists.filter(id=subcategory.id).exists(),
         'quizzes': quizzes,
         'quiz_results': quiz_results,
    }
    return render(request, 'side_bar/playlists.html', context)


def like_video(request, id):
    video = get_object_or_404(Videos, id=request.GET.get('like_video_id'))
    if video.likes_num.filter(id=request.user.id).exists():
        video.likes_num.remove(request.user)
    else:
        video.likes_num.add(request.user)
    
    return HttpResponseRedirect(reverse('watch_video', args=[str(id)]))

def watch_video_view(request, id):
    video = get_object_or_404(Videos.objects.all(), id=id)
    comments = Comments.objects.filter(video=video).order_by('created_at')[:5]
    new_comment = None
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.video = video
            new_comment.user = request.user
            new_comment.save()
            video.increment_comments()
            return redirect('watch_video', id=id)
    else:
        form = CommentForm()

    liked = False
    if video.likes_num.filter(id=request.user.id).exists():
        liked = True

    context = {
        'video': video,
        'form': form,
        'comments': comments,
        'number_of_likes': video.number_of_likes(),
        'video_is_liked': liked
    }
    
    return render(request, 'pages/watch_video.html', context)


class SearchResultsView(ListView):
    model = Subcategory
    template_name = 'pages/search.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get('search')
        return Subcategory.objects.filter(
            Q(name__icontains=query) | Q(descriptions__icontains=query)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('search')
        return context