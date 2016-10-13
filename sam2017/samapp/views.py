from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AuthorForm, UserLoginForm
from django.contrib import auth


# Create your views here.
def index(request):
    return render(request, 'samapp/index.html', context_instance=RequestContext(request))


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('samapp/login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return HttpResponseRedirect('/accounts/invalid')


def loggedin(request):
    return render_to_response('samapp/loggedin.html',{'fullname' : request.user.username})


def invalid_login(request):
    return render_to_response('samapp/invalid_login.html')


def logout(request):
    auth.logout(request)
    return render_to_response('samapp/logout.html')


def register_user(request):
    form = AuthorForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register_success')

        args = {}
        args.update(csrf(request))

        args['form'] = AuthorForm()
        return render_to_response('samapp/register.html', args)


def register_success(request):
    render_to_response('register_success.html')





