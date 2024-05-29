from django.shortcuts import render, redirect
from .models import Comments, Videos

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
