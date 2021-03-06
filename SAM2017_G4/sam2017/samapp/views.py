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
from django.db.models import Q

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
def assignments(request):
    user = PCM.objects.get(user=request.user)
    paper = Paper.objects.filter(Q(pcm1 = user)| Q(pcm2 = user) | Q(pcm3=user))

    context = {
        'paper': paper
    }
    return render_to_response('assignments.html',context)

@login_required
def selections(request):
    paper = Selection.objects.all()
    context = {
        'paper': paper
    }
    return render_to_response('selections.html',context)


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
            notiftype = form.cleaned_data['title']
            notif_count = NotificationTemp.objects.filter(title=notiftype)
            if len(notif_count)==0:
                newNotif = form.save(commit=False)
                newNotif.save()
            else:
                notif_count.delete()
                newNotif = form.save(commit=False)
                newNotif.save()

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
            deadlinetype = form.cleaned_data['deadlineType']
            deadline = (request.POST.get('deadline'))
            deadline_count = Deadline.objects.filter(deadlineType=deadlinetype)
            if len(deadline_count)==0:
                newdeadline = form.save(commit=False)
                newdeadline.save()
            else:
                deadline_count.delete()
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
            deadlines =get_object_or_404(Deadline, deadlineType='paperSubmission')
            #deadline_val=deadlines[0]
            # deadline_val=deadlines[0]
            submissiondate=utc.localize(datetime.now())
            # print('if ',str(submissiondate) > str(deadline_val))
            if submissiondate < deadlines.deadline:

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


def is_member(user):
    return user.groups.filter(name='PCM').exists()


def is_member1(user):
    return user.groups.filter(name='PCC').exists()


def paperselected(request):
    return render_to_response('paperselected.html')


@user_passes_test(is_member)
@login_required
def pcmpapers(request):
    user = request.user
    pcm = PCM.objects.get(user=user)
    paper_info=Paper.objects.all()

    paper_data={
        'paper_detail':paper_info
    }
    context = {
        'pcm': pcm,
        'paper': paper_info,
    }


    if request.method=='POST':#request.POST.get('Rate'):
        paper = request.POST.get('RequestID')
        paper1 = Paper.objects.get(pk=paper)
        selectionlist = Selection.objects.all().filter(PCM=pcm, selected_papers=paper1)
        context['slist'] = selectionlist
        if selectionlist:
            return HttpResponseRedirect('/paperselected/')

        elif not selectionlist and 'Selected' in request.POST:
            selection = Selection.create(pcm, paper1)
            return HttpResponseRedirect('/pcmpapers/')


    else:
        variables = RequestContext(request)

        return render_to_response('pcmpapers.html', context, variables)

    return render_to_response('pcmpapers.html', context)





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

@user_passes_test(is_member1)
@csrf_protect
@login_required
def assignpapers(request, paper_id):
    doc = Paper.objects.get(pk = paper_id)
    pcms = PCM.objects.all()
    selection = Selection.objects.all()
    context = {
        'selection': selection,
        'pcm': pcms,
        'paper': doc
    }

    if request.method == 'POST' and 'Assigned' in request.POST:
        pcm1 = request.POST.get('PCMa')
        pcm1_a = PCM.objects.get(pk=pcm1)
        pcm2 = request.POST.get('PCMb')
        pcm2_a = PCM.objects.get(pk=pcm2)
        pcm3 = request.POST.get('PCMa')
        pcm3_a = PCM.objects.get(pk=pcm3)

        if pcm1 != pcm2 !=pcm3:

            doc.pcm1 = pcm1_a
            doc.pcm2 = pcm2_a
            doc.pcm3 = pcm3_a
            doc.assigned = True

            doc.save()
            pcma = PCM.objects.get(pk=pcm1)
            pcmb = PCM.objects.get(pk=pcm2)
            pcmc = PCM.objects.get(pk=pcm3)

            notification = Notification()
            recipients = [pcma.user, pcmb.user, pcmc.user]
            notification.sendNotification("assigntoReview", recipients)

            return HttpResponseRedirect('../../pccpapers/')

        elif pcm1 == pcm2 or pcm2 == pcm3 or pcm1 == pcm3:
            return HttpResponseRedirect('../../failassignment/')


    return render_to_response('assignpapers.html', context_instance=RequestContext(request, context))

def successassignment(request):
    return render_to_response('successassignment.html')

def failassignment(request):
    return render_to_response('failassignment.html')

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
    # deadline_val = deadlines[0]
    currentDate = utc.localize(datetime.now())

    # if the method is POST and rating has to be saved
    if request.method=='POST' or '/PCM_review/' in request.POST:
        print('inside POst')
        print('deadline', currentDate , deadlines.deadline)
        if currentDate<deadlines.deadline:


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
    # deadline_val = deadlines[0]
    currentDate = utc.localize(datetime.now())
    print('deadline', currentDate, deadlines.deadline)
    if request.method == 'POST' and 'Rate' in request.POST:


        if currentDate<deadlines.deadline:


            form = PccForm(request.POST)
            if form.is_valid():
                rate = form.cleaned_data['rate']

                doc.rate = rate
                doc.save()


            return HttpResponseRedirect('/pccpapers')
        else:
            return HttpResponseRedirect('/Deadline_Error/')

    elif request.method =='POST' and 'Conflict' in request.POST:
        if currentDate < deadlines.deadline:
            review1=Review.objects.get(id=review.id)
            review1.grade=0
            review1.save()
            return HttpResponseRedirect('/pccpapers/')
        else:
            return HttpResponseRedirect('/Deadline_Error/')
    else:
        form = PccForm()

    return render_to_response('PCCreview.html',context_instance=RequestContext(request,{'form':form}))
