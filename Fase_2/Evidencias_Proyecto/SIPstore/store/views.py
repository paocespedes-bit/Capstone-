from django.shortcuts import render
from .models import PaneleSIP, KitConstruccion


#! Aqui se agregan las views (templates).

def paneles(request):
    paneles = PaneleSIP.objects.all()
    return render(request, 'paneles.html',{"paneles":paneles})

def catalogo_kits(request):
    kits = KitConstruccion.objects.all()
    return render(request, "t_kit.html",{"kits":kits})





