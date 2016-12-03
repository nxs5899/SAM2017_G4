from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
# Register your models here.


from .models import Author, Paper, Review, Samadmin, PCC, PCM,Deadline,Notification,NotificationTemp
from .forms import AuthorForm, PaperForm


class AuthorAdmin(admin.ModelAdmin):
    class Meta:
        model = Author

class PaperAdmin(admin.ModelAdmin):
    class Meta:
        model = Paper

admin.site.register(Author, AuthorAdmin)
admin.site.register(Paper)
admin.site.register(Review)
admin.site.register(Samadmin)
admin.site.register(PCC)
admin.site.register(PCM)
admin.site.register(Deadline)
admin.site.register(Notification)
admin.site.register(NotificationTemp)