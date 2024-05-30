from django.shortcuts import render, redirect, get_object_or_404
from .models import Comments, Videos, Subcategory
from users.models import Profile

def add_comment(request, video_id):
    video = Videos.objects.get(pk=video_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video = video
            comment.user = request.user
            comment.save()
            return redirect('video_detail', video_id=video_id)
    else:
        form = CommentForm()
        context = {
            'form': form
        }
    return render(request, 'add_comment.html', context)

def save_playlist_view(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    profile = request.user.profile
    if profile.saved_playlists.filter(id=subcategory.id).exists():
        profile.saved_playlists.remove(subcategory)
    else:
        profile.saved_playlists.add(subcategory)
    return redirect('playlists_view', id=subcategory_id)
