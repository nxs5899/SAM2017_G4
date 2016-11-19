# views.py
from django.conf.global_settings import MEDIA_ROOT

from samapp.forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from sam2017.settings import MEDIA_ROOT
from django.contrib.auth.models import User, Group


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
            g = Group.objects.get(name='author')
            g.user_set.add(user)
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
@csrf_protect
def create_admin(request):

    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )

            samadmin = Samadmin(
                user=user,
                fname=form.cleaned_data['fname'],
                lname=form.cleaned_data['lname']
            )

            user.save()
            samadmin.save()
            g = Group.objects.get(name='admin')
            g.user_set.add(user)
            return HttpResponseRedirect('/register/success/')
    else:
        form = AdminForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'registration/registeradmin.html',
        variables,
    )

    

def register_success(request):
    return render_to_response(
        'registration/success.html',
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def is_member2(user):
    return user.groups.filter(name='admin').exists()

@user_passes_test(is_member2)
@login_required
def createpcc(request):

    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )

            pcc = PCC(
                user=user,
                fname=form.cleaned_data['fname'],
                lname=form.cleaned_data['lname']
            )

            user.save()
            pcc.save()
            g = Group.objects.get(name='PCC')
            g.user_set.add(user)
            return HttpResponseRedirect('/home/')
    else:
        form = AdminForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'createpcc.html',
        variables,
    )

@user_passes_test(is_member2)
@login_required
def createpcm(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )

            pcm = PCM(
                user=user,
                fname=form.cleaned_data['fname'],
                lname=form.cleaned_data['lname']
            )

            user.save()
            pcm.save()
            g = Group.objects.get(name='PCM')
            g.user_set.add(user)
            return HttpResponseRedirect('/home/')
    else:
        form = AdminForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'createpcm.html',
        variables,
    )

@user_passes_test(is_member2)
@login_required
def manageaccounts(request):
    user = request.user
    pccusers = PCC.objects.all()
    pcmusers = PCM.objects.all()

    context = {
        'PCC': pccusers,
        'PCM': pcmusers
    }
    if request.method == 'POST' and 'Deactivate' in request.POST:
        username = request.POST.get('RequestID')
        user2 = User.objects.get(pk=username)
        user2.is_active = False
        user2.save()
        return HttpResponseRedirect('/manageaccounts/')

    elif request.method == 'POST' and 'Activate' in request.POST:
        username = request.POST.get('RequestID')
        user2 = User.objects.get(pk=username)
        user2.is_active = True
        user2.save()

        return HttpResponseRedirect('/manageaccounts/')

    return render_to_response('manageaccounts.html', context_instance=RequestContext(request, context))

@user_passes_test(is_member2)
@login_required
def UpdateUser(request, user_id):
    user = User.objects.get(pk= user_id)

   # try:
    #userProfile = UserProfile.objects.get(user = user)

    #except:
    #user1 = request.user
    #userProfile1 = UserProfile.objects.get(user = user1)
    #notification = checkRequest(userProfile1)

    if request.method == 'POST' and 'Save' in request.POST:
        form = AdminForm(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            userProfile.first_Name = form.cleaned_data['first_Name']
            userProfile.last_Name = form.cleaned_data['last_Name']
            userProfile.zipCode = form.cleaned_data['zipCode']
            userProfile.address = form.cleaned_data['address']
            userProfile.pickupArrangements = form.cleaned_data['pickupArrangements']
            userProfile.date = form.cleaned_data['date1']
            user.save()
            userProfile.save()
            variables = RequestContext(request, {
                'form': form
            })
            return HttpResponseRedirect('/ManageUsers/')
    else:
        form = AdminForm()
        form.fields['username'].initial = user.username
        form.fields['email'].initial = user.email
        form.fields['first_Name'].initial = userProfile.first_Name
        form.fields['last_Name'].initial = userProfile.last_Name
        form.fields['zipCode'].initial = userProfile.zipCode
        form.fields['address'].initial = userProfile.address
        form.fields['pickupArrangements'].initial = userProfile.pickupArrangements
        form.fields['date1'].initial = userProfile.date
    return render_to_response('UpdateUser.html', context_instance=RequestContext(request,
                                                                                             {'form': form,
                                                                                              'notification': notification}))


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
    current_pcc = User.objects.filter(groups__name='PCC')
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
            notification = Notification()
            recipients = [user, current_pcc]
            notification.sendNotification("PaperSubmitted", recipients)

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
        print("")
        # Need to have some functionality for this
    return render_to_response('SubmittedPapers.html',context)

def is_member(user):
    return user.groups.filter(name='PCM').exists()

@user_passes_test(is_member)
@login_required
def pcmpapers(request):
    paper_info=Paper.objects.all()
    paper_data={
        'paper_detail':paper_info
    }
    context = {
        'paper': paper_info,
    }


    return render_to_response('pcmpapers.html',context)

def is_member1(user):
    return user.groups.filter(name='PCC').exists()

@user_passes_test(is_member1)
@login_required
def pccpapers(request):
    paper_info=Paper.objects.all()
    paper_data={
        'paper_detail':paper_info
    }
    context = {
        'paper': paper_info,
    }


    return render_to_response('pccpapers.html',context)

@login_required
def downloadPDF(request, paper_id):
    doc = Paper.objects.get(pk=paper_id)
    title = doc.title
    version = doc.version
    formats = doc.formats
    document = doc.document

    context = {
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


@login_required
def show_notification(request):
    notifications = Notification.objects.filter(recipients = request.user.pk)

    user = get_object_or_404(User, pk=request.user.pk)
    return render(request, 'view-notifications.html',{'notifications':notifications,'user':user})

@login_required
def review_Rate_PCM(request):
    '''
    pCM rate
    :param request:
    :return:
    '''

    context=RequestContext(request)
    reviewer = Review.objects.all()#(reviewer=reviewer,paperId=paper)# change to current user
    paper_info = Paper.objects.get(pk=1)# fetch paper id from pcm page

    context=RequestContext(request)


    # if the method is POST and rating has to be saved
    if request.method=='POST' or '/PCM_review/' in request.POST:
        print('inside POst')

        # reviewer.paperId=paprer_info#request.POST.get('title')
        grade=request.POST.get('rating')
        print(grade)
        comments=request.POST.get('comments')
        review1=Review.create(paper_info,grade,comments)

        return render_to_response('PCM_review.html', context_instance=RequestContext(request))
        # return render_to_response('pcmpapers.html', context)
        # return pcmpapers(request)

    else:
        context['title']=paper_info
        return render_to_response('PCM_review.html', context)

