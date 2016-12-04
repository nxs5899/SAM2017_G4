# views.py
from django.conf.global_settings import MEDIA_ROOT

from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from .models import *
# from sam2017.settings import MEDIA_ROOT
from django.contrib.auth.models import User, Group
from datetime import datetime
import pytz
from django.utils import timezone

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
    if request.method == 'POST' and 'DeactivatePCC' in request.POST:
        username = request.POST.get('RequestID')
        user2 = User.objects.get(pk=username)
        user2.is_active = False
        user2.save()
        return HttpResponseRedirect('/manageaccounts/')

    elif request.method == 'POST' and 'ActivatePCC' in request.POST:
        username = request.POST.get('RequestID')
        user2 = User.objects.get(pk=username)
        user2.is_active = True
        user2.save()

        return HttpResponseRedirect('/manageaccounts/')

    elif request.method == 'POST' and 'DeactivatePCM' in request.POST:
        username = request.POST.get('RequestID1')
        user3 = User.objects.get(pk=username)
        user3.is_active = False
        user3.save()

        return HttpResponseRedirect('/manageaccounts/')

    elif request.method == 'POST' and 'ActivatePCM' in request.POST:
        username = request.POST.get('RequestID1')
        user3 = User.objects.get(pk=username)
        user3.is_active = True
        user3.save()

        return HttpResponseRedirect('/manageaccounts/')
    return render_to_response('manageaccounts.html', context_instance=RequestContext(request, context))


@user_passes_test(is_member2)
@login_required
def UpdatePCC(request, user_id):
    user = User.objects.get(pk= user_id)
    userProfile = PCC.objects.get(user = user)
    user1 = request.user
    userProfile1 = Samadmin.objects.get(user = user1)

    if request.method == 'POST' and 'Save' in request.POST:
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            userProfile.fname = form.cleaned_data['fname']
            userProfile.lname = form.cleaned_data['lname']
            user.save()
            userProfile.save()
            variables = RequestContext(request, {
                'form': form
            })
            return HttpResponseRedirect('/manageaccounts/')
    else:
        form = UserProfileForm()
        form.fields['username'].initial = user.username
        form.fields['email'].initial = user.email
        form.fields['fname'].initial = userProfile.fname
        form.fields['lname'].initial = userProfile.lname
    return render_to_response('UpdateUser.html', context_instance=RequestContext(request,
                                                                                             {'form': form}))

@user_passes_test(is_member2)
@login_required
def UpdatePCM(request, user_id):
    user = User.objects.get(pk= user_id)
    userProfile = PCM.objects.get(user = user)
    user1 = request.user
    userProfile1 = Samadmin.objects.get(user = user1)

    if request.method == 'POST' and 'Save' in request.POST:
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            userProfile.fname = form.cleaned_data['fname']
            userProfile.lname = form.cleaned_data['lname']
            user.save()
            userProfile.save()
            variables = RequestContext(request, {
                'form': form
            })
            return HttpResponseRedirect('/manageaccounts/')
    else:
        form = UserProfileForm()
        form.fields['username'].initial = user.username
        form.fields['email'].initial = user.email
        form.fields['fname'].initial = userProfile.fname
        form.fields['lname'].initial = userProfile.lname
    return render_to_response('UpdateUser.html', context_instance=RequestContext(request,
                                                                                             {'form': form}))




@login_required
def home(request):
    return render_to_response(
        'home.html',
        {'user': request.user}
    )

@login_required
def Deadline_Error(request):
    return render_to_response(
        'Deadline_Error.html',
        {'user': request.user}
    )


@login_required
def NotifTemp(request):
    user = request.user
    if request.method == 'POST' and 'submittemp' in request.POST:
        form = NotifTemForm(request.POST)
        if form.is_valid():
            template = NotificationTemp(
                                         title=form.cleaned_data['title'],
                                         message=form.cleaned_data['message'],
                                       )
            template.save()

            return HttpResponseRedirect('/notiftemp/')

    else:
        form = NotifTemForm()
        variables = RequestContext(request, {'form': form })

    return render_to_response('notiftemp.html', context_instance=RequestContext(request,{'form': form}))


@login_required
def Deadlines(request):
    user = request.user
    if request.method == 'POST' and 'submitdeadline' in request.POST:
        form = DeadlineForm(request.POST)
        if form.is_valid():
            deadlineType = form.cleaned_data['deadlineType']
            deadline = (request.POST.get('deadline'))
            newdeadline = form.save(commit=False)
            newdeadline.save()
            # newdeadline = Deadline(
            #                              deadlineType=form.cleaned_data['deadlineType'],
            #                              deadline=form.cleaned_data['deadline'],
            #                            )
            # newdeadline.save()

            return HttpResponseRedirect('/deadline/')

    else:
        form = DeadlineForm()
        variables = RequestContext(request, {'form': form })

    return render_to_response('deadline.html', context_instance=RequestContext(request,{'form': form}))


@login_required
def SubmitPaper(request):
    user = request.user
    author = Author.objects.get(user=user)
    utc=pytz.UTC

    # current_pcc = User.objects.filter(groups__name='PCC')
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
            # check if the deadline for papersubmission--To-Do
            deadlines =Deadline.objects.filter(deadlineType='paperSubmission')
            deadline_val=deadlines[0]
            submissiondate=utc.localize(datetime.now())
            # print('if ',str(submissiondate) > str(deadline_val))
            if submissiondate < deadline_val.deadline:

                paper.save()
                notification = Notification()
                recipients = [user]
                notification.sendNotification("paperSubmitted", recipients)

                return HttpResponseRedirect('/SubmittedPapers/')
            else:
                return HttpResponseRedirect('/Deadline_Error/')

    else:
        form = PaperForm()
        variables = RequestContext(request, {'form': form })

    return render_to_response('submitpaper.html', context_instance=RequestContext(request,{'form': form}))


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



    if request.method=='POST':#request.POST.get('Rate'):
        print('in pcmpapers')

        context['title']=request.POST.get('Rate')
        return render_to_response('PCM_review.html', context)

    else:


        return render_to_response('pcmpapers.html',context)
    #


def is_member1(user):
    return user.groups.filter(name='PCC').exists()

@user_passes_test(is_member1)
@login_required
def pccpapers(request):
    context=RequestContext(request)
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
    notifications = Notification.objects.filter(recipient=request.user.pk)

    user = get_object_or_404(User, pk=request.user.pk)
    return render(request, 'view-notifications.html',{'notifications':notifications,'user':user})

@login_required
def review_Rate_PCM(request, paper_id):
    '''
    pCM rate
    :param request:
    :return:
    '''
    doc = Paper.objects.get(pk = paper_id)
    context=RequestContext(request)
    reviewer = Review.objects.all()#(reviewer=reviewer,paperId=paper)# change to current user
    paper_info = Paper.objects.get(pk=doc.id)# fetch paper id from pcm page
    utc = pytz.UTC
    deadlines = Deadline.objects.filter(deadlineType='paperReview')
    deadline_val = deadlines[0]
    currentDate = utc.localize(datetime.now())

    # if the method is POST and rating has to be saved
    if request.method=='POST' or '/PCM_review/' in request.POST:
        print('inside POst')
        print('deadline', currentDate , deadline_val.deadline)
        if currentDate<deadline_val.deadline:


            # reviewer.paperId=paprer_info#request.POST.get('title')
            grade=request.POST.get('rating')
            print(grade)
            comments=request.POST.get('comments')
            print("user id is",(request.user))
            pcm=PCM.objects.get(user=request.user)
            print("user id is", (pcm))
            review1=Review.create(paper_info,grade,comments,pcm)

            # return render_to_response('PCM_review.html', context_instance=RequestContext(request))
            return render_to_response('Home.html', context)
        else:
            return HttpResponseRedirect('/Deadline_Error/')
        # return pcmpapers(request)

    else:
        context['title']=paper_info
        return render_to_response('PCM_review.html', context)



@user_passes_test(is_member1)
@login_required
def review_PCC(request, paper_id):
    utc = pytz.UTC
    doc = Paper.objects.get(pk=paper_id)
    context = RequestContext(request)
    # reviewer = Review.objects.all()  # (reviewer=reviewer,paperId=paper)# change to current user
    #paper_info = Paper.objects.get(pk=doc.id)  # fetch paper id from pcm page


    review = Review.objects.get(id=doc.id)
    print(review.grade)


    # for object in review:
    #
    #     if object.paperId==doc:
    #         print('inside if',doc,object)
    #         print(object.reviewer)
    #         context = {
    #             'paper': doc,
    #             'Review': review
    #         }


    print(request.method)
    deadlines = Deadline.objects.filter(deadlineType='paperRate')
    deadline_val = deadlines[0]
    currentDate = utc.localize(datetime.now())
    print('deadline', currentDate, deadline_val.deadline)
    if request.method == 'POST' and 'Rate' in request.POST:


        if currentDate<deadline_val.deadline:


            form = PccForm(request.POST)
            if form.is_valid():
                rate = form.cleaned_data['rate']

                doc.rate = rate
                doc.save()


            return HttpResponseRedirect('/pccpapers')
        else:
            return HttpResponseRedirect('/Deadline_Error/')

    elif request.method =='POST' and 'Conflict' in request.POST:
        if currentDate < deadline_val.deadline:
            review1=Review.objects.get(id=review.id)
            review1.grade=0
            review1.save()
            return HttpResponseRedirect('/pccpapers/')
        else:
            return HttpResponseRedirect('/Deadline_Error/')
    else:
        form = PccForm()

    return render_to_response('PCCreview.html',context_instance=RequestContext(request,{'form':form}))
