__author__ = 'Nick'
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from SecureWitness.models import SiteUser
from SecureWitness.forms import UserForm, FolderForm, GroupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.template.response import TemplateResponse
import os

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
	reports = Report.objects.filter(owner=request.user)
	for report in reports:
		rep_dict[report]= report.file_set.all()
	folders = Folder.objects.filter(owner=request.user)
	return render(request, 'profile.html', {'reports':reports,'rep_dict':rep_dict,'folders':folders},context_instance=RequestContext(request))

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
				print('adding folder')
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
			report.public=request.POST.get('public',False)
			report.save()
			if request.FILES:
				for f in request.FILES.getlist('docfiles'):
					report.file_set.create(docfile=f)
					report.save()
			return redirect('SecureWitness.views.profile')
	else:
		form = ReportForm(initial={'short_des':report.short_des,'long_des':report.long_des,'location':report.location,'date':report.incident_date,'public':report.public})
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
def report_view(request, report_id, file_id=-1):
	report = get_object_or_404(Report,pk=report_id)
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
	return render(request, 'report.html', {'report':report,'file_dict':file_dict})

@login_required
def folder_view(request,folder_id):
	folder = get_object_or_404(Folder,pk=folder_id)
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