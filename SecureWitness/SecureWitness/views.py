__author__ = 'Nick'
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from SecureWitness.forms import UserForm, User, FolderForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
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