__author__ = 'Nick'
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from SecureWitness.models import SiteUser
from SecureWitness.forms import UserForm, FolderForm, GroupForm, AddUserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.template.response import TemplateResponse
from django.core.mail import send_mail
from SecureWitness.forms import SearchForm
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
import os
import copy
from SecureWitness.models import Report, File, Folder
from SecureWitness.forms import ReportForm


def index(request):
    return render_to_response('index.html')

def home(request):
    return render_to_response('home.html')

@login_required
def submit(request):
	if request.method == 'POST' and request.user.is_authenticated():
		form = ReportForm(request.POST, request.FILES)
		if form.is_valid():
			newRep = Report(owner = request.user, short_des = request.POST['short_des'], long_des = request.POST['long_des'], location = request.POST['location'], incident_date = request.POST['date'],public = request.POST.get('public',False))
			newRep.save()
			if request.FILES:
				for f in request.FILES.getlist('docfiles'):
					newRep.file_set.create(docfile=f)
					newRep.save()
			return redirect('SecureWitness.views.submitted')
	else:
		form = ReportForm()
	Reports = Report.objects.all()
	return render_to_response(
		'submit.html',
		{'form': form},
		context_instance=RequestContext(request)
	)

@login_required
def profile(request):
	rep_dict={}
	rep_dict2={}
	groups = request.user.groups.all()
	reports = set()
	for group in groups:
		for rep in group.report_set.all():
			reports.add(rep)
	reports2 = (Report.objects.filter(owner=request.user) | Report.objects.filter(userviewers__username=request.user.username))
	for report in reports2:
		if report in reports:
			reports.remove(report)
	for report in reports:
		rep_dict[report]= report.file_set.all()
	for report in reports2:
		rep_dict2[report]= report.file_set.all()
	folders = Folder.objects.filter(owner=request.user)
	return render(request, 'profile.html', {'reports':reports,'reports2':reports2,'rep_dict':rep_dict,'rep_dict2':rep_dict2,'folders':folders,'crntuser':request.user},context_instance=RequestContext(request))

@login_required
def remote_profile(request):
	rep_dict={}
	rep_dict2={}
	groups = request.user.groups.all()
	reports = set()
	for group in groups:
		for rep in group.report_set.all():
			reports.add(rep)
	reports2 = (Report.objects.filter(owner=request.user) | Report.objects.filter(userviewers__username=request.user.username))
	for report in reports:
		rep_dict[report]= report.file_set.all()
	for report in reports2:
		rep_dict2[report]= report.file_set.all()
	folders = Folder.objects.filter(owner=request.user)
	return render(request, 'remoteAccessProfile.html', {'reports':reports,'reports2':reports2,'rep_dict':rep_dict,'rep_dict2':rep_dict2,'folders':folders,'crntuser':request.user},context_instance=RequestContext(request))

def custom_proc(request):
    return {
        'dictionary': request.reports
    }
@login_required
def createfolder(request):
	if request.method == 'POST':
		form = FolderForm(request.POST)
		newFol = Folder(owner=request.user,title=request.POST['title'])
		newFol.save()
		for key in request.POST:
			if key.startswith('r_') and request.POST[key]=='on':
				rep = Report.objects.get(pk=int(key[2:]))
				rep.folder.add(newFol)
				rep.save()
				newFol.save()
			if key.startswith('f_') and request.POST[key]=='on':
				fol = Folder.objects.get(pk=int(key[2:]))
				fol.ofolder.add(newFol)
				fol.save()
				newFol.save()
		return redirect('SecureWitness.views.profile')
	else:
		form = FolderForm()
	reports = Report.objects.filter(owner=request.user)
	folders = Folder.objects.filter(owner=request.user)
	return render(request,'createfolder.html',{'form':form,'reports':reports,'folders':folders})

@login_required
def editreport(request,report_id):
	report = Report.objects.get(pk=report_id)
	if request.method=="POST":
		form = ReportForm(request.POST, request.FILES)
		if form.is_valid():
			report.file_set.all().delete()
			report.short_des=request.POST['short_des']
			report.long_des=request.POST['long_des']
			report.location=request.POST['location']
			report.incident_date=request.POST['date']
			report.keywords=request.POST['keywords']
			report.public=request.POST.get('public',False)
			report.save()
			if request.FILES:
				for f in request.FILES.getlist('docfiles'):
					report.file_set.create(docfile=f)
					report.save()
			return redirect('SecureWitness.views.profile')
	else:
		form = ReportForm(initial={'short_des':report.short_des,'long_des':report.long_des,'location':report.location,'date':report.incident_date,'keywords':report.keywords,'public':report.public})
	context={'report':report,'form':form}
	return render(request,'editreport.html',context)


@login_required
def editfolder(request,folder_id):
	fol = Folder.objects.get(pk=folder_id)
	if request.method=="POST":
		for report in Report.objects.filter(owner=request.user):
			if ('r_'+str(report.id)) in request.POST:
				report.folder.add(fol)
			else:
				report.folder.remove(fol)
			report.save()
			fol.save()
		for fold in Folder.objects.filter(owner=request.user):
			if ('f_'+str(fold.id)) in request.POST:
				fold.ofolder.add(fol)
			else:
				fold.ofolder.remove(fol)
			fold.save()
			fol.save()
		return redirect('SecureWitness.views.profile')
	reports = Report.objects.filter(owner=request.user)
	rep_set = fol.report_set.all()
	folders = Folder.objects.filter(owner=request.user)
	fol_set = fol.ofolder.all()
	context = {'folder':fol,'reports':reports,'rep_set':rep_set,'folders':folders,'fol_set':fol_set}
	return render(request,'editfolder.html',context)

@login_required
def grantpermissions(request, report_id):
	report = get_object_or_404(Report,pk=report_id)
	if not report.canview(request.user):
		return HttpResponse("You cannot grant permissions for this report")
	if request.method == 'POST':
		if Group.objects.filter(name=request.POST['topermit']).exists():
			report.groupviewers.add(Group.objects.get(name=request.POST['topermit']))
		elif SiteUser.objects.filter(username=request.POST['topermit']).exists():
			report.userviewers.add(SiteUser.objects.get(username=request.POST['topermit']))
		else:
			return render(request, 'permitdne.html',{'report':report})
		return redirect('SecureWitness.views.profile')
	else:
		return render(request, 'grantpermissions.html', {'report':report})

@login_required
def report_view(request, report_id, file_id=-1):
	report = get_object_or_404(Report,pk=report_id)
	if not report.canview(request.user):
		return HttpResponse("You cannot view this report")
	file_dict = {}
	if request.method == 'POST':
		report.delete()
		return redirect('SecureWitness.views.profile')
	if file_id:
		f = get_object_or_404(File,pk=file_id)
		response = HttpResponse(f.docfile,content_type='application/force-download')
		display = f.docfile.url.split('/')[-1]
		response['Content-Disposition']='attachment; filename=%s' % str(display)
		return response
	for f in report.file_set.all():
		file_dict[f] = f.docfile.url.split('/')[-1]
	return render(request, 'report.html', {'report':report,'file_dict':file_dict,'crntuser':request.user})

@login_required
def folder_view(request,folder_id):
	folder = get_object_or_404(Folder,pk=folder_id)
	if not (folder.owner == request.user):
		return HttpResponse("You cannot view with folder.")
	rep_dict = {}
	fol_dict = {}
	if request.method == 'POST':
		folder.delete()
		return redirect('SecureWitness.views.profile')
	for rep in folder.report_set.all():
		rep_dict[rep]=rep.id
	print(folder.ofolder.all())
	for fol in folder.ofolder.all():
		fol_dict[fol]=fol.id
	return render(request, 'folder.html',{'folder':folder,'rep_dict':rep_dict,'fol_dict':fol_dict})

@login_required
def submitted(request):
	return render(request, 'submitted.html')

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = SiteUser.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password'])
            user.save()
            subject = "Thank you for Registering"
            msg = """
            	Thank you for creating your account with SecureWitness.
            	We hope you enjoy your safe and secure stay, %s
            """ % user.username
            print (msg)
            send_mail(subject,msg, "Secure Witness <securewitness17@gmail.com>",[user.email],fail_silently=False,auth_user="securewitness17@gmail.com",auth_password="serverpassword")
            registered = True
        else:
            print(user_form.errors)
        return redirect('SecureWitness.views.user_login')
    else:
        user_form = UserForm()

    return render(request, 'register.html', {'user_form' : user_form, 'registered' : registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('SecureWitness.views.home')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Login failed")
    else:
        return render(request, 'login.html', {})

@login_required()
def create_group(request):
    if request.method == 'POST':
        group_form = GroupForm(data=request.POST)

        if group_form.is_valid():
            group = Group.objects.get_or_create(name=request.POST.get('name'))

        else:
            print(group_form.errors)
        return redirect('SecureWitness.views.home')
    else:
        group_form = GroupForm()

    return render(request, 'creategroup.html', {'group_from' : group_form})


class SearchListView(ListView):
    model = SearchForm





def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            searchText = form.cleaned_data['searchText']
            foundReports = searching(searchText, request.user)
            return render(request, 'results.html', {'reports': foundReports})
    else:
        form = SearchForm()
        return render(request, 'search.html', {'form': form, })

def results(request):
    return render(request, 'results.html')


def searching(find, user):
    report_set = set
    # try:
    looking = Report.objects.filter(short_des__contains=find) | Report.objects.filter(long_des__contains=find) | Report.objects.filter(location__contains=find) | Report.objects.filter(keywords__contains=find)
    userfind = SiteUser.objects.filter(username=find)
    if userfind:
	    looking = looking | Report.objects.filter(owner=userfind)
    for report in copy.deepcopy(looking):
        if not report.canview(user):
            looking.remove(report)
    return looking

@login_required()
def add_user_to_group(request):

    if request.method == 'POST':
        add_user_form = AddUserForm(data=request.POST)

        if add_user_form.is_valid():
            user_to_add = SiteUser.objects.get(username=request.POST.get('username'))
            group = Group.objects.get(name=request.POST.get('groupname'))
            if (request.user in group.user_set.all()):
                group.user_set.add(user_to_add)

        else:
            print(add_user_form.errors)
        return redirect('SecureWitness.views.add_user_to_group')
    else:
        add_user_form = AddUserForm()

    return render(request,'addusertogroup.html',{'add_user_form' : add_user_form})

