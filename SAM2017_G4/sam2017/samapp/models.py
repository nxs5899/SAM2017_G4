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

class PCM(models.Model):
    user = models.OneToOneField(User)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return str(self.fname) + ' ' + str(self.lname)

class PCC(models.Model):
    user = models.OneToOneField(User)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return str(self.fname) + ' ' + str(self.lname)

class Samadmin(models.Model):
    user = models.OneToOneField(User)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

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

    def ratePaper(self, rate):
        self.rate = rate

        self.save()

    def __str__(self):
        return self.title
		



class NotificationTemp(models.Model):
    messageTypes = (
        ('paperSubmitted', 'paperSubmitted'),
        ('selectpaper', 'selectpaper'),
        ('assigntoReview', 'assigntoReview'),
        ('startReview', 'startReview'),
        ('reviewComplete', 'reviewComplete'),
        ('paperRate', 'paperRate'),
    )

    title = models.CharField(max_length=500, choices=messageTypes)
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + '' + self.message


class Deadline(models.Model):
    deadlineTypes = (
        ('paperSubmission', 'paperSubmission'),
        ('paperSelection', 'paperSelection'),
        ('paperAssign', 'paperAssign'),
        ('paperReview', 'paperReview'),
        ('paperRate', 'paperRate'),
    )

    deadlineType = models.CharField(max_length=500, choices=deadlineTypes)
    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.deadline)


class Notification(models.Model):
    title = models.CharField(max_length=500, verbose_name=u"Title")
    message = models.CharField(max_length=500)
    viewed = models.BooleanField(default=False, verbose_name=u"Viewd?")
    recipient = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + '' + self.message

    # notification_message_mapper = {
    #     "PaperSubmitted": " Your paper was successfully submitted. Check your notification bar for updates.",
    #     "SelectPaper": "Please select papers to review.",
    #     "Selection Complete": "Please assign papers to PCMs.",
    #     "PaperAssigned": "The papers is assigned to you. Please start your review.",
    #     "ReviewComplete": "Reviews are complete. Please check them.",
    #     "PaperRate": "Your paper has been rated.",
    # }
    #
    # def _constructNotificationMessage(self, message):
    #     # paper = Paper.objects.get(pk=paperid)
    #     custom_message = message
    #     #print("Changes message ??? ", custom_message)
    #     return custom_message

    def sendNotification(self, type, recipients):
        newmessage = NotificationTemp.objects.get(title=type)
        notification = self
        notification.title = type
        #print("message " + self.notification_message_mapper[type])
<<<<<<< HEAD:sam2017/samapp/models.py
        notification.message = newmessage.message
=======
        notification.message = newmessage.message# added .message to save the message
>>>>>>> 144ab38a0162e2515326a330186a98a41c546088:SAM2017_G4/sam2017/samapp/models.py
        #self._constructNotificationMessage(self.notification_message_mapper[type])
        #print("constructed message " + notification.message)
        notification.save()
        notification.recipient.set(recipients)
        notification.save()



class Review(models.Model):
    '''
    Model for Review
    author: smruthi
    '''
    paperId=models.ForeignKey(Paper)
    reviewer=models.ForeignKey(PCM)
    grade=models.IntegerField(null=True)
    comments=models.TextField()
    submissiondate=models.DateTimeField(auto_now_add=True)
    submissionDeadline=models.DateTimeField(auto_now_add=True)# change this after deadlines are set
    def __str__(self):
        return str(self.pk)

    @classmethod
    def create(cls,paperId,grade,comments,reviewer):
        reviewPaper=cls(paperId=paperId,grade=grade,comments=comments,reviewer=reviewer)

        reviewPaper.save()
        return reviewPaper



