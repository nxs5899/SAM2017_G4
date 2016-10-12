from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
# Register your models here.


from .models import Author, Paper
from .forms import AuthorForm, PaperForm


class AuthorAdmin(admin.ModelAdmin):
    class Meta:
        model = Author

admin.site.register(Author, AuthorAdmin)
