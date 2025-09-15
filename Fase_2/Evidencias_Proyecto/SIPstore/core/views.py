from django.shortcuts import render
from django.http import HttpResponse
from store.models import PaneleSIP


#! Aqui se agregan las views (templates).

def index(request):
    paneles = PaneleSIP.objects.all()
    return render(request, 'index.html',{"paneles":paneles})