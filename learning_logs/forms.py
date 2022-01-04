from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class EntryForm(forms.Form):
    text = forms.CharField(max_length=200, label='text', widget=forms.TextInput(
        attrs={'placeholder': 'Chapter title'}))
    page_number = forms.IntegerField(label='page number')
    chapter_number = forms.IntegerField(label='chapter number')


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email',)
