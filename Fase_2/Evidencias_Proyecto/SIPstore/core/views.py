from django.shortcuts import render
from django.http import HttpResponse
from store.models import PanelSIP,KitConstruccion


#! Aqui se agregan las views (templates).

def index(request):
    paneles = PanelSIP.objects.all().order_by('-id')[:10]
    kits = KitConstruccion.objects.all().order_by('-id')[:10]
    
    context = {
        'paneles': paneles,
        'kits': kits
    }
    return render(request, 'index.html', context)