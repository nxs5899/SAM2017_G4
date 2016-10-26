import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from samapp.models import *


class AuthorForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label=_("Username"), error_messages={
            'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Password (again)"))
    fname = forms.CharField(max_length=25)
    lname = forms.CharField(max_length=25)

    class Meta:
        model = Author
        exclude = ('user')

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

<<<<<<< HEAD
    def getUsername(self):
        return self.username

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password1
=======
>>>>>>> 4dd9b8507d44a3b661b0901dbb4d780c70eedb0f

class PaperForm(forms.Form):
    formatChoices = (
        ('PDF', 'PDF'),
        ('Word', 'Word'),
    )


    submitter = forms.CharField(max_length=255)
    title = forms.CharField(max_length=255)
    version = forms.FloatField()
    formats = forms.ChoiceField(choices=formatChoices, required=True)

    def validate_file_extension(self):
        import os
        ext = os.path.splitext(self.name)[1]
        valid_extensions = ['.pdf', '.docx']
        if not ext in valid_extensions:
            raise forms.ValidationError(_('Please upload a pdf or doc file'), code='invalid')

    paper = forms.FileField(validators=[validate_file_extension], error_messages={'invalid':_("Please upload a pdf or doc file")})