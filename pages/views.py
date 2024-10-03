from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from courses.models import Category, Subcategory, Videos, Likes, Comments
from django.contrib.auth.models import User
from users.models import Teachers, Profile, AdminIncome
from .forms import CommentForm
from courses.models import Comments
from quiz_app.models import Quiz
from results.models import Result
from django.views.generic import ListView
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from decimal import Decimal

from users.forms import ReviewForm
from users.models import Review, PurchasedPlaylist

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
    subcategory_count = Subcategory.objects.count()
    users_count = User.objects.count()
    teachers_count = Teachers.objects.count()
    reviews = Review.objects.all().order_by('-created_at')[:6]

    if request.method == 'POST':
        if request.user.is_authenticated:  # Foydalanuvchining login qilganligini tekshiramiz
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                messages.success(request, "Sharhingiz muvaffaqiyatli qo'shildi!")
                return redirect('about_page')
        else:
            messages.error(request, "Sharh qoldirish uchun avval saytga kirishingiz kerak.")
            return redirect('login')  # Foydalanuvchini login sahifasiga yo'naltiramiz
    else:
        form = ReviewForm()

    # 5-star rating uchun ro'yxat hosil qilamiz
    star_range = range(1, 6)

    context = {
        'subcategory_count': subcategory_count,
        'users_count': users_count,
        'teachers_count': teachers_count,
        'reviews': reviews,
        'form': form,
        'star_range': star_range,  # Bu ro'yxatni templatega uzatamiz
    }
    return render(request, 'side_bar/about.html', context)


def contact_me_view(request):
    return render(request, 'side_bar/contact.html')


def tutor_contact_view(request):
    return render(request, 'pages/tutor_contact.html')

def courses_view(request):
    courses = Subcategory.objects.all().order_by('-created_at')
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

@login_required()
def playlists_view(request, id):
    subcategory = get_object_or_404(Subcategory.objects.all(), id=id)
    quizzes = Quiz.objects.filter(topic=subcategory)
    profile = request.user.profile

    # Foydalanuvchi subkategoriyani sotib olganmi yoki yo'qligini tekshirish
    is_purchased = PurchasedPlaylist.objects.filter(user=request.user, subcategory=subcategory).exists()



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
         'is_purchased': is_purchased,
         'quizzes': quizzes,
         'quiz_results': quiz_results,
    }
    return render(request, 'side_bar/playlists.html', context)

def playlists_done(request, id):
    subcategory = get_object_or_404(Subcategory, id=id)
    return render(request, 'payment/payment_done.html', context={'subcategory': subcategory})


def playlist_pay(request, id):
    subcategory = get_object_or_404(Subcategory, id=id)
    profile = request.user.profile

    # Foydalanuvchi balansini tekshirish
    if profile.balance >= subcategory.price:
        # Balansdan narxni yechish
        profile.balance -= subcategory.price
        profile.save()  # Yangi balansni saqlash

        # Xaridni `PurchasedPlaylist` modeliga yozish
        PurchasedPlaylist.objects.create(user=request.user, subcategory=subcategory)

        # Daromadlarni hisoblash
        teacher_income = Decimal(subcategory.price) * Decimal('0.60')
        admin_income = Decimal(subcategory.price) * Decimal('0.40')

        # O'qituvchining daromadini yangilash
        teacher = subcategory.teacher  # O'qituvchini subkategoriya orqali olish
        teacher.income += teacher_income
        teacher.save()

        # Adminning daromadini yangilash
        admin_profile = Profile.objects.filter(user__is_superuser=True).first()
        if admin_profile:
            # Admin daromad obyektini yaratishda income qiymatini ham ko'rsatamiz
            admin_income_obj, created = AdminIncome.objects.get_or_create(
                profile=admin_profile,
                defaults={'income': admin_income}
            )
            if not created:
                # Agar obyekt allaqachon mavjud bo'lsa, daromadni yangilaymiz
                admin_income_obj.income += admin_income
                admin_income_obj.save()

        # Xaridni tasdiqlash va foydalanuvchini playlistga qaytarish
        messages.success(request, "Xaridingiz uchun rahmat!")
        return redirect('playlists_view', id=id)
    else:
        # Mablag' yetarli bo'lmagan holat
        messages.error(request, "Hisobingizda mablag' yetarli emas!")
        return redirect('playlists_view', id=id)



@login_required
def earning_list(request):
    # Foydalanuvchi admin yoki teacher bo'lishini tekshirish
    if not (hasattr(request.user, 'teacher') or request.user.is_staff):
        messages.error(request, "Sizga bu sahifaga kirishga ruxsat yo'q.")
        return redirect('home_page')  # Redirect qilingan sahifani yozing

    # Xarid qilingan kurslar ro'yxatini olish
    purchased_playlists = PurchasedPlaylist.objects.select_related('subcategory', 'user')

    # Agar foydalanuvchi o'qituvchi bo'lsa, o'z subcategorylaridan xarid qilingan kurslarni olish
    if hasattr(request.user, 'teacher') and not request.user.is_staff:
        purchased_playlists = purchased_playlists.filter(subcategory__teacher=request.user.teacher)

    total_teacher_income = 0
    total_admin_income = 0

    # Har bir xarid bo'yicha daromadlarni hisoblash
    for purchase in purchased_playlists:
        teacher_income = purchase.subcategory.price * 0.6  # O'qituvchi daromadi (60%)
        admin_income = purchase.subcategory.price * 0.4  # BioOlam daromadi (40%)

        total_teacher_income += teacher_income
        total_admin_income += admin_income

    context = {
        'purchased_playlists': purchased_playlists,
        'total_teacher_income': total_teacher_income,
        'total_admin_income': total_admin_income,
    }

    return render(request, "earnings/earnings_list.html", context)



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


def to_pay(request):
    return render(request, 'payment/to_pay.html')