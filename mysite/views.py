# Create your views here.
from django.shortcuts import render

def start(request):
    return render(request, 'start.html')
    
def about(request):
    return render(request, 'about.html')
    
def help(request):
    return render(request, 'help.html')
    
