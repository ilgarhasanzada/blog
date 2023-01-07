from django.shortcuts import render
from .models import About

def home(request):
    try:
        description = About.objects.all()[0].description
    except:
        description="Information does'nt exists."
    return render(request, 'home.html', {"description": description})
