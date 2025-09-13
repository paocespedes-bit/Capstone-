from django.shortcuts import render
from django.http import HttpResponse


#! Aqui se agregan las views (templates).

def paneles(request):
    return render(request, 'paneles.html')




