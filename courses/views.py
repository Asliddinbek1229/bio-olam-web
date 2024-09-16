from django.shortcuts import render, redirect, get_object_or_404
from .models import Comments, Videos, Subcategory
from users.models import Profile, Teachers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import SubcategoryForm, VideoForm


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

# New subcategory
@login_required(login_url='login')
def add_subcategory(request):
    if not hasattr(request.user, 'teacher'):
        return HttpResponseForbidden("Sizga Kurs qo'shish uchun ruxsat berilmagan!")

    if request.method == 'POST':
        form = SubcategoryForm(request.POST, request.FILES)
        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.teacher = request.user.teacher
            subcategory.save()
            return redirect('home_page')

    else:
        form = SubcategoryForm()
    return render(request, 'teachers/add_subcategory.html', {'form': form})

@login_required(login_url='login')
def edit_subcategory(request, id):
    subcategory = get_object_or_404(Subcategory, id=id)

    if request.user.teacher != subcategory.teacher:
        return HttpResponseForbidden("Siz faqat o'zingiz qo'shgan kurslarni tahrirlay olasiz!")

    if request.method == 'POST':
        form = SubcategoryForm(request.POST, request.FILES, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('home_page')
    else:
        form = SubcategoryForm(instance=subcategory)
    return render(request, 'teachers/edit_subcategory.html', {'form': form})

@login_required(login_url='login')
def delete_subcategory(request, id):
    subcategory = get_object_or_404(Subcategory, id=id)

    if request.user.teacher != subcategory.teacher:
        return HttpResponseForbidden("Siz faqat o'zingiz qo'shgan subkategoriyalarni o'chirishingiz mumkin.")

    if request.method == 'POST':
        subcategory.delete()
        return redirect('home_page')
    return render(request, 'teachers/delete_subcategory.html', {'subcategory': subcategory})

# Video qo'shish tahrirlash o'chirish uchun
@login_required(login_url='login')
def add_video(request):
    user_subcategory = Subcategory.objects.filter(teacher=request.user.teacher)

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            if video.subcategory.teacher != request.user.teacher:
                return HttpResponseForbidden("Bu Kursga video qo'sha olmaysiz!!!")
            video.save()
            return redirect('home_page')

    else:
        form = VideoForm()
    return render(request, 'teachers/add_video.html', {'form': form})

@login_required
def edit_video(request, id):
    video = get_object_or_404(Videos, id=id)

    if video.subcategory.teacher != request.user.teacher:
        return HttpResponseForbidden("Siz bu videoni tahrirlashga ruxsatingiz yo'q.")

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('home_page')
    else:
        form = VideoForm(instance=video)
    return render(request, 'teachers/edit_video.html', {'form': form})

@login_required
def delete_video(request, id):
    video = get_object_or_404(Videos, id=id)

    if video.subcategory.teacher != request.user.teacher:
        return HttpResponseForbidden("Siz bu videoni o'chirishga ruxsatingiz yo'q.")

    if request.method == 'POST':
        video.delete()
        return redirect('home_page')
    return render(request, 'teachers/delete_video.html', {'video': video})

@login_required
def videos_list(request):
    videos = Videos.objects.filter(subcategory__teacher=request.user.teacher)
    return render(request, 'teachers/videos_list.html', {'videos': videos})