from django.shortcuts import render
from django.http import HttpResponse


#! Aqui se agregan las views (templates).

def index(request):
    return render(request, 'index.html')