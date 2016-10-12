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
from .forms import AuthorForm

# Create your views here.

def register_author(request):
    if request.POST:
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/samapp/index');
    else:
        form = AuthorForm()
    args = {}
    args.update(csrf(request))
    args['form']=form
    return render_to_response('samapp/register_author.html', args, context_instance=RequestContext(request))
