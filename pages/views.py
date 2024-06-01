from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from courses.models import Category, Subcategory, Videos, Likes, Comments
from .forms import CommentForm
from courses.models import Comments

from django.http import JsonResponse

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
    return render(request, 'side_bar/about.html')

def contact_me_view(request):
    return render(request, 'side_bar/contact.html')

def courses_view(request):
    courses = Subcategory.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'side_bar/courses.html', context)

def playlists_view(request, id):
    subcategory = get_object_or_404(Subcategory.objects.all(), id=id)
    profile = request.user.profile

    if request.method == 'POST':
        if profile.saved_playlists.filter(id=subcategory.id).exists():
            profile.saved_playlists.remove(subcategory)
        else:
            profile.saved_playlists.add(subcategory)
        return redirect('playlists_view', id=id)
    
    videos = subcategory.videos_set.all()
    context = {
        'subcategory': subcategory,
        'videos': videos,
         'is_saved': profile.saved_playlists.filter(id=subcategory.id).exists()
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


