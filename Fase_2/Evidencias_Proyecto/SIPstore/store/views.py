from django.shortcuts import render
from .models import PanelSIP, KitConstruccion


#! Aqui se agregan las views (templates).

def paneles(request):
    paneles = PanelSIP.objects.all()
    context = {
        'paneles': paneles,
        # 'kits': kits
    }
    return render(request, 'paneles.html',context)

def catalogo_kits(request):
    kits = KitConstruccion.objects.all()
    context = {
        # 'paneles': paneles,
        'kits': kits
    }
    return render(request, "t_kit.html",context)





