__author__ = 'Nick'
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from SecureWitness.models import Report
from SecureWitness.forms import ReportForm

def index(request):
    return render_to_response('index.html')

def home(request):
    return render_to_response('home.html')

def submit(request):
	if request.method == 'POST':
		form = ReportForm(request.POST, request.FILES)
		if form.is_valid():
			newRep = Report(reporter = request.POST['reporter'], title = request.POST['title'], docfile = request.FILES['docfile'])
			newRep.save()
			return HttpResponseRedirect('http://127.0.0.1:8000/submitted/')
	else:
		form = ReportForm()
	Reports = Report.objects.all()
	return render_to_response(
		'submit.html',
		{'Reports': Reports, 'form': form},
		context_instance=RequestContext(request)
	)

def list(request):
	reports = Report.objects.all()
	return render(request, 'list.html', {'reports':reports})

def submitted(request):
	return render(request, 'submitted.html')