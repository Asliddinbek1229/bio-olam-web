from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from courses.models import Category, Subcategory, Videos
from .forms import CommentForm
from courses.models import Comments

# Create your views here.
def home_page(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all().order_by('-created_at')[:6]
    context = {
        'categories': categories,
        'subcategories': subcategories
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
    videos = subcategory.videos_set.all()
    context = {
        'subcategory': subcategory,
        'videos': videos
    }
    return render(request, 'side_bar/playlists.html', context)

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
            return redirect('watch_video', id=id)
    else:
        form = CommentForm()
    context = {
        'video': video,
        'form': form,
        'comments': comments
    }
    return render(request, 'pages/watch_video.html', context)


