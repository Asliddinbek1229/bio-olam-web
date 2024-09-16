from django import forms
from .models import Subcategory, Videos

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['category', 'name', 'descriptions', 'image', 'course_type', 'price', 'old_price']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Videos
        fields = ['subcategory', 'name', 'description', 'time', 'video', 'cover_image']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Foydalanuvchini olish, agar mavjud bo'lsa
        super().__init__(*args, **kwargs)
        if user:
            # Subkategoriyalarni faqat ushbu foydalanuvchi o'zi yaratganlarini ko'rsatish uchun filtr
            self.fields['subcategory'].queryset = Subcategory.objects.filter(teacher=user.teacher)