from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import logout, authenticate, login
from .forms import LoginForm, CustomPasswordChangeForm, UserRegisterForm
from django.views import generic
from django.contrib import messages


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data['username'],
                password=data['password']
            )

            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, "Tizimga muvaffaqiyatli kirildi")
                return redirect('home_page')
            else:
                messages.error(request, "Login yoki parolda xatolik bor!!!")
        else:
            messages.error(request, "Login va parol noto'g'ri kiritildi!!!")
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'registration/login.html', context)


def dashboard_view(request):
    user = request.user
    context = {
        user: user
    }
    return render(request, 'pages/dashboard.html', context)


class CustomPasswordChangeView(generic.FormView):
    form_class = CustomPasswordChangeForm
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home_page')
