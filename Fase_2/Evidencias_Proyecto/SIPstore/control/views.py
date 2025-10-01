from django.shortcuts import render
from store.models import PanelSIP, KitConstruccion, Categoria


#! Aqui se agregan las views (templates).
def control(request):
    return render(request, 'home_control.html')

def stock(request):
    paneles = PanelSIP.objects.all()
    kits = KitConstruccion.objects.all()
    categorias = Categoria.objects.all()
    context = {
        'paneles': paneles,
        'kits': kits,
        'categorias' : categorias,
    }
    return render(request,'stock.html',context)
