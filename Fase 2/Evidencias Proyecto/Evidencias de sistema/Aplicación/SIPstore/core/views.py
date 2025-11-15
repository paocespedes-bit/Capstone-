from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import PanelSIP,KitConstruccion,Resena
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

def index(request):
    
    limpiar_resenas_no_revisadas()

    condicion_pedido = Q(inventario__modo_stock='pedido')
    condicion_stock_disponible = Q(
        inventario__modo_stock='stock',
        inventario__disponible__gt=0
    )

    paneles = PanelSIP.objects.filter(
        condicion_pedido | condicion_stock_disponible
    ).order_by('-id')[:10]

    kits = KitConstruccion.objects.filter(
        condicion_pedido | condicion_stock_disponible
    ).order_by('-id')[:10]

    ultimas_resenas = Resena.objects.filter(
        revisado=True
    ).order_by('-fecha_comentario')[:5]

    context = {
        'paneles': paneles,
        'kits': kits,
        'ultimas_resenas': ultimas_resenas,
    }

    return render(request, 'index.html', context)

def agregar_resena(request):
    if request.method == "POST":
        autor = request.POST.get("autor", "Cliente")
        texto = request.POST.get("texto")
        if texto:
            Resena.objects.create(autor=autor, texto=texto)
    return redirect("home")  

def limpiar_resenas_no_revisadas():
    limite_fecha = timezone.now() - timedelta(days=7)
    Resena.objects.filter(revisado=False, fecha_comentario__lt=limite_fecha).delete()
