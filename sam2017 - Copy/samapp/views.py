# views.py
from samapp.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )

            author = Author(
            user = user,
            fname = form.cleaned_data['fname'],
            lname = form.cleaned_data['lname']
            )

            user.save()
            author.save()
            return HttpResponseRedirect('/register/success/')
    else:
        form = AuthorForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'registration/register.html',
        variables,
    )


def register_success(request):
    return render_to_response(
        'registration/success.html',
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def home(request):
    return render_to_response(
        'home.html',
        {'user': request.user}
    )


@login_required
def SubmitPaper(request):
    user = request.user
    author = Author.objects.get(user=user)

    if request.method == 'POST' and 'submitpaper' in request.POST:
        form = PaperForm(request.POST, request.FILES)
        if form.is_valid():
            paper = Paper(contact_author = author,
                                         title=form.cleaned_data['title'],
                                         submitter=form.cleaned_data['submitter'],
                                         version=form.cleaned_data['version'],
                                         formats=form.cleaned_data['formats'],
                                         document=form.cleaned_data['document']
                                         )
            paper.save()
            return HttpResponseRedirect('/SubmittedPapers/')

    else:
        form = PaperForm()
        variables = RequestContext(request, {
        'form': form })

    return render_to_response('submitpaper.html', context_instance=RequestContext(request,
        {'form': form}))


def successpaper(request):
    return render_to_response(
        'successpaper.html',
    )

@login_required
def submittedpapers(request):
    author = Author.objects.get(user=request.user)
    paper_info=Paper.objects.all()
    paper_data={
        'paper_detail':paper_info
    }
    try:
        context = {'authorId':author.id}
        papers = Paper.objects.all()
        for object in papers:
            if object.contact_author_id == author.id:
                print (object.submitter)
                print(object.title)
                print(object.version)
                print(object.formats)
                print(object.document)
                context['papers'] = papers

    except ObjectDoesNotExist:
        print("Need to show the user that they haven't created the tables till now.")
        # Need to have some functionality for this
    return render_to_response('SubmittedPapers.html',context)

@login_required
def downloadPDF(request):
    user = request.user
    author = Author.objects.get(user=user)
    doc = Paper.objects.get(contact_author=author)
    title = doc.title
    version = doc.version
    formats = doc.formats
    document = doc.document

    context = {
        'user':user,
        'author': author,
        'doc':doc,
        'title':title,
        'version': version,
        'formats': formats,
        'document': document
    }

    if 'PDF' == doc.formats:
        image_data = open(MEDIA_ROOT+'/'+doc.document.name, 'rb').read()
        return HttpResponse(image_data, content_type='application/pdf')
    else:
        image_data = open(MEDIA_ROOT+'/'+doc.document.name, 'rb').read()
        return HttpResponse(image_data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')