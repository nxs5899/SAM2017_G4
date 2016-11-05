from django.db import models
from django.core.validators import RegexValidator
from django import forms
from django.forms import ModelForm
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return str(self.fname) + ' ' + str(self.lname)


class Paper(models.Model):
    formatChoices = (
        ('PDF', 'PDF'),
        ('Word', 'Word'),
    )

    contact_author = models.ForeignKey(Author)
    submitter = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    version = models.FloatField()
    formats = models.CharField(max_length=5, choices=formatChoices)  # find the enumerate field for word and PDF
    document = models.FileField()
    rate = models.FloatField(default=None, null=True)
    sub_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-title"]

    def __str__(self):
        return self.title


class Notification(models.Model):
    title = models.CharField(max_length=500, verbose_name=u"Title")
    message = models.TextField(verbose_name=u"Message")
    viewed = models.BooleanField(default=False, verbose_name=u"Viewd?")
    recipient = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + '' + self.message

    notification_message_mapper = {
        "PaperSubmitted": " dear Author, your paperId was successfully submitted. check ur not bar for later updates",
        "SelectPaper": "dear PCMs, plz select papers to review ",
        "SelectionComplete": "dear PCC, plz assign papers to PCMs",
        "PaperAssigned": "dear PCMs, the paperId is assigned to you. plz start your review.",
        "ReviewComplete": "dear PCC reviews are complete. plz check",
        "PaperRate": "dear Author, ur paperId is rated.",
    }

    def _constructNotificationMessage(self, message):
        # paper = Paper.objects.get(pk=paperid)
        custom_message = message
        #print("Changes message ??? ", custom_message)
        return custom_message

    def sendNotification(self, type, recipients):
        notification = self
        notification.title = type
        #print("message " + self.notification_message_mapper[type])
        notification.message = self._constructNotificationMessage(self.notification_message_mapper[type])
        #print("constructed message " + notification.message)
        notification.save()
        notification.recipient.set(recipients)
        notification.save()