"""sam2017 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""


from django.conf.urls import patterns, include, url
from samapp.views import *
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^admin/',admin.site.urls), 
                       url(r'^$', 'django.contrib.auth.views.login'),
                       url(r'^logout/$', logout_page),
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
                       # If user is not login it will redirect to login page
                       url(r'^register/$', register),
                       url(r'^registeradmin/$', create_admin),
                       url(r'^register/success/$', register_success),
                       url(r'^home/$', home),
                       url(r'^submitpaper/$', SubmitPaper),
                       url(r'^notiftemp/$', NotifTemp),
                       url(r'^deadline/$', Deadlines),
                       url(r'^successpaper/$', successpaper),
                       url(r'^SubmittedPapers/$', submittedpapers),
                       url(r'^(?P<paper_id>[0-9]+)/downloadPDF/$', downloadPDF, name='downloadPDF'),
                       url(r'^pcmpapers/$', pcmpapers),
                       url(r'^pccpapers/$', pccpapers),
                       url(r'^notifications/$', show_notification),
                       url(r'^createpcc/$', createpcc),
                       url(r'^createpcm/$', createpcm),
                       url(r'^manageaccounts/$', manageaccounts),
                       # url(r'^(?P<user_id>[0-9]+)/UpdateUser/$', UpdateUser, name='UpdateUser'),
                       url(r'^(?P<user_id>[0-9]+)/UpdatePCC/$', UpdatePCC, name='UpdatePCC'),
                       url(r'^(?P<user_id>[0-9]+)/UpdatePCM/$', UpdatePCM, name='UpdatePCM'),
					   url(r'^(?P<paper_id>[0-9]+)/PCM_review/$', review_Rate_PCM, name='ReviewPCM'),
					   url(r'^(?P<paper_id>[0-9]+)/PCCreview/$', review_PCC, name='ReviewPCC'),
                       url(r'^Deadline_Error/$', Deadline_Error),
                       url(r'^(?P<paper_id>[0-9]+)/assignpapers/$', assignpapers, name='assignpapers'),
                       url(r'^successassignment/$', successassignment),
                       url(r'^failassignment/$', failassignment),
                       url(r'^assignments/$', assignments),
                       url(r'^selections/$', selections),
                       url(r'^paperselected/$', paperselected),
                       )