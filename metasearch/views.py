# Create your views here.
from django.shortcuts import render

def start(request):
    return render(request, 'metasearch/start.html')

def about(request):
	return render(request, 'metasearch/about.html')

def help(request):
	return render(request, 'metasearch/help.html')
