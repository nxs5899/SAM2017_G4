from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from .models import Author, Deadline,Paper,Review


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
    fname = forms.CharField(max_length=25, label=_("First Name"))
    lname = forms.CharField(max_length=25, label=_("Last Name"))

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

    def getUsername(self):
        return self.username

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password1


class AdminForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label=_("Username"), error_messages={
            'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Password (again)"))
    fname = forms.CharField(max_length=25, label=_("First Name"))
    lname = forms.CharField(max_length=25, label=_("Last Name"))

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

    def getUsername(self):
        return self.username

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password1

class UserProfileForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(max_length=30)), label=_("Email address"))
    fname = forms.CharField(max_length=25)
    lname = forms.CharField(max_length=25)


class PaperForm(forms.Form):
    formatChoices = (
        ('PDF', 'PDF'),
        ('Word', 'Word'),
    )
    submitter = forms.CharField(max_length=255)
    title = forms.CharField(max_length=255)
    version = forms.FloatField()
    formats = forms.ChoiceField(choices=formatChoices, required=True)
    document = forms.FileField()

    def clean(self):
        try:
            document = self.cleaned_data['document']
        except KeyError:
            raise forms.ValidationError(_('Please upload a paper.'), code='invalid')
        if self.cleaned_data['formats'] == 'PDF':
            if '.pdf' not in self.cleaned_data['document'].name:
                 raise forms.ValidationError(_("You have selected the PDF format. Please upload a PDF document or change the format"))
        elif self.cleaned_data['formats'] == 'Word':
             if not self.cleaned_data['document'].name.endswith('.docx') and not self.cleaned_data['document'].name.endswith('.doc'):
                 raise forms.ValidationError(_("You have selected the Word format. Please upload a Word document or change the format."))
        else:
            raise forms.ValidationError(_("Please upload a pdf or word document."))
        return self.cleaned_data

class PccForm(forms.Form):
    rate = forms.CharField(max_length=25)
	
class NotifTemForm(forms.Form):
    messageTypes = (
        ('paperSubmitted', 'paperSubmitted'),
        ('selectpaper', 'selectpaper'),
        ('assigntoReview', 'assigntoReview'),
        ('startReview', 'startReview'),
        ('reviewComplete', 'reviewComplete'),
        ('paperRate', 'paperRate'),
    )
    title = forms.ChoiceField(choices=messageTypes, required=True)
    message = forms.CharField(max_length=500)

    def clean(self):
        # try:
        #     document = self.cleaned_data['document']
        # except KeyError:
        #     raise forms.ValidationError(_('Please provide the messages.'), code='invalid')

        return self.cleaned_data



class DeadlineForm(forms.ModelForm):

    class Meta:
        model = Deadline
        fields = ('deadlineType', 'deadline')
        # widgets = {'deadline': forms.DateInput(attrs={'class':'datepicker'})}
    # deadlineTypes = (
    #     ('paperSubmission', 'paperSubmission'),
    #     ('paperSelection', 'paperSelection'),
    #     ('paperAssign', 'paperAssign'),
    #     ('paperReview', 'paperReview'),
    #     ('paperRate', 'paperRate'),
    # )
    #
    # deadlineType = forms.ChoiceField(choices=deadlineTypes)
    # deadline = forms.DateTimeField()
    #
    # def clean(self):
    #     # try:
    #     #     document = self.cleaned_data['document']
    #     # except KeyError:
    #     #     raise forms.ValidationError(_('Please provide the messages.'), code='invalid')
    #
    #     return self.cleaned_data