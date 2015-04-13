__author__ = 'Nick'
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from SecureWitness.forms import UserForm, User
from django.contrib.auth import authenticate, login

import os

from SecureWitness.models import Report, File
from SecureWitness.forms import ReportForm


def index(request):
    return render_to_response('index.html')

def home(request):
    return render_to_response('home.html')

def submit(request):
	if request.method == 'POST':
		form = ReportForm(request.POST, request.FILES)
		if form.is_valid():
			print("form is valid")
			newRep = Report(reporter = request.POST['reporter'], short_des = request.POST['short_des'], long_des = request.POST['long_des'], location = request.POST['location'], incident_date = request.POST['date'],public = request.POST.get('public',False))
			newRep.save()
			print (request.FILES)
			if request.FILES.get('docfile',False):
				newRep.file_set.create(encrypt_file = request.POST.get('encrypt_file',False),docfile = request.FILES['docfile'])
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

def list(request):
	rep_dict={}
	reports = Report.objects.all()
	for report in reports:
		rep_dict[report]= report.file_set.all()
	return render(request, 'list.html', {'reports':reports,'rep_dict':rep_dict})

def report_view(request, report_id, file_id=-1):
	report = get_object_or_404(Report,pk=report_id)
	file_dict = {}
	if request.method == 'POST':
		report.delete()
		return redirect('SecureWitness.views.list')
	if file_id:
		file = get_object_or_404(File,pk=file_id)
		response = HttpResponse(file.docfile,content_type='application/force-download')
		response['Content-Disposition']='attachment; filename=%s' % str(file.report.short_des)
		return response
	for file in report.file_set.all():
		file_dict[file] = os.path.abspath(file.docfile.url)
	return render(request, 'report.html', {'report':report,'file_dict':file_dict})

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
                return HttpResponseRedirect('SecureWitness.views.home')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Login failed")
    else:
        return render(request, 'login.html', {})