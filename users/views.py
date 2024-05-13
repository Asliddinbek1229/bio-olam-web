from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from .forms import LoginForm


# Create your views here.
def user_login(request):
    msg = ''  # <-- Yangi qatordan oldin msg ni e'lon qiling
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            user = authenticate(
                request,
                username=data['username'],
                password=data['password']
            )

            if user is not None and user.is_active:  # <--- is_active ni funksiya sifatida chaqirish
                login(request, user)
                return redirect('home_page')
            else:
                msg = "Sizning profilingiz faol holatda emas!!!"
        else:
            msg = "Login yoki parolda xatolik bor!!!"
    else:
        form = LoginForm()

    context = {'msg': msg, 'form': form}  # <-- context ni bo'shatish

    return render(request, 'registration/login.html', context)  # <-- response qaytarish



def register_user(request):
    ...


def logout_view(request):
    logout(request)
    return redirect('home_page')
