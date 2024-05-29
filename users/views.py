from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import logout, authenticate, login
from .forms import LoginForm, CustomPasswordChangeForm, UserRegisterForm, UserEditForm, ProfileEditForm, TeacherForm
from django.views import generic
from django.contrib import messages

from courses.models import Category, Subcategory, Videos, Comments

from .models import Profile, Teachers


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
            Profile.objects.create(user=new_user)
            messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home_page')


def edit_user_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Muvaffaqiyatli tahrirlandi!")
            return redirect('dashboard_user')
        else:
            messages.error(request, "Tahrirlashda xatolik bor!!!")
            return redirect('dashboard_user')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
    
    return render(request, 'pages/edit_user_profile.html', context)


def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_page')  # O'qituvchilar ro'yhatini ko'rish sahifasiga qaytish
    else:
        form = TeacherForm()
    return render(request, 'registration/add_teacher.html', {'form': form})


def teachers_view(request):
    teachers = Teachers.objects.all()
    context = {
        'teachers': teachers
    }
    return render(request, 'teachers/teachers.html', context)

def teacher_profiles_view(request, id):
    teacher = get_object_or_404(Teachers.objects.all(), id=id)
    subcategories = Subcategory.objects.filter(teacher=teacher)
    context = {
        'teacher': teacher,
        'subcategories': subcategories
    }
    return render(request, 'teachers/teacher_profile.html', context)

