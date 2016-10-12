from django.db import models
from django import forms
from django.forms import ModelForm
from .models import Author, Paper
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class PaperForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
