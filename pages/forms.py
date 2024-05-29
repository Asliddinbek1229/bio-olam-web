# forms.py

from django import forms
from courses.models import Comments

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
