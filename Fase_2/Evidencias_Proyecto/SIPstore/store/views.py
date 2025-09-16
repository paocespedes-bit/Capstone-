from django.shortcuts import render
from .models import PanelSIP, KitConstruccion


#! Aqui se agregan las views (templates).

def paneles(request):
    paneles = PanelSIP.objects.all()
    context = {
        'paneles': paneles,
        
    }
    return render(request, 'paneles.html',context)

def kits(request):
    kits = KitConstruccion.objects.all()
    context = {
        
        'kits': kits
    }
    return render(request, "kits.html",context)





