from django.shortcuts import render
from courses.models import Category, Subcategory, Videos

# Create your views here.
def home_page(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
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
    return render(request, 'side_bar/courses.html')

def playlists_view(request):
    return render(request, 'side_bar/playlists.html')