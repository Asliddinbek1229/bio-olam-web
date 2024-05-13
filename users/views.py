from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import logout

# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'


def logout_view(request):
    logout(request)
    return redirect('home')
