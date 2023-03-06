from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def suggestion(request):
    return render(request,"ai/suggestion.html",{})

def explore(request):
    return render(request,"ai/explore.html",{})