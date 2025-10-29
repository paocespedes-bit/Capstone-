from django.shortcuts import render
from django.http import HttpResponse
from store.models import PanelSIP,KitConstruccion
from django.db.models import Q

#! Aqui se agregan las views (templates).

def index(request):
    condicion_pedido = Q(inventario__modo_stock='pedido')
    condicion_stock_disponible = Q(inventario__modo_stock='stock', inventario__disponible__gt=0)
    
    
    paneles = PanelSIP.objects.filter(
        condicion_pedido | condicion_stock_disponible
    ).order_by('-id')[:10]
    
    kits = KitConstruccion.objects.filter(
        condicion_pedido | condicion_stock_disponible
    ).order_by('-id')[:10]
    
    context = {
        'paneles': paneles,
        'kits': kits
    }
    return render(request, 'index.html', context)