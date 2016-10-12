from django.conf.urls import url
from . import views

app_name = 'samapp'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?i)', views.register_author, name='register'),
    ]


