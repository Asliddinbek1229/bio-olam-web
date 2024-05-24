from django.shortcuts import render

# Create your views here.
def contact_me_view(request):
    return render(request, 'side_bar/contact.html')

def courses_view(request):
    return render(request, 'courses/courses.html')
