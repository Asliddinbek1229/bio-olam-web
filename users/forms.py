from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Profile, Teachers

from .validators import validate_not_too_similar, validate_not_common_password, validate_not_entirely_numeric


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    old_password = forms.CharField(
        label="Eski parol",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label="Yangi parol",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=(
            "Parol kamida 8 ta belgi uzunlikda bo'lishi kerak.<br>"
            "Parol sizning shaxsiy ma'lumotlaringizga juda o'xshash bo'lishi mumkin emas.<br>"
            "Parol keng tarqalgan parol bo'lishi mumkin emas.<br>"
            "Parol faqat raqamlardan iborat bo'lishi mumkin emas."
        ),
        validators=[validate_not_too_similar, validate_not_common_password, validate_not_entirely_numeric]
    )
    new_password2 = forms.CharField(
        label="Yangi parolni tasdiqlang",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if len(password1) < 8:
            raise forms.ValidationError("Parol kamida 8 ta belgi uzunlikda bo'lishi kerak.")
        return password1

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label="Parol", 
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label="Parolni takrorlang", 
                                widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') != data.get('password2'):
            raise forms.ValidationError("Parolingiz bir-biriga mos kelmadi!!!")
        return data.get('password2')
    

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'date_of_birth', 'job', 'bio']
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'job': forms.Select(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teachers
        fields = ['user', 'teacher_type', 'bio',]