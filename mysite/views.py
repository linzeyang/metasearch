# Create your views here.
from django.shortcuts import render_to_response

def start(request):
    return render_to_response('start.html')
    
def about(request):
    return render_to_response('about.html')
    
def help(request):
    return render_to_response('help.html')
    
