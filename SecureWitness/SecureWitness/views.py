__author__ = 'Nick'
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

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
	repDict={}
	reports = Report.objects.all()
	for report in reports:
		repDict[report]= report.file_set.all()
	return render(request, 'list.html', {'reports':reports,'repDict':repDict})

def report_view(request, report_id):
	report = get_object_or_404(Report,pk=report_id)
	if request.method == 'POST':
		report.delete()
	return render(request, 'report.html', {'report':report})

def submitted(request):
	return render(request, 'submitted.html')