__author__ = 'Nick'
from django.shortcuts import render_to_response

def index(request):
    return render_to_response('index.html')

def home(request):
    return render_to_response('home.html')

def submit(request):
    return render_to_response('submit.html')