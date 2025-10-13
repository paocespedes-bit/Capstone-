from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
import json
from store.models import PanelSIP, KitConstruccion 

# Create your views here.
def carrito(request):
    carrito = request.session.get("carrito", [])

    # Calculamos subtotal por producto y total general
    total = 0
    for item in carrito:
        item['subtotal'] = item['precio_unitario'] * item['cantidad']
        total += item['subtotal']

    context = {
        'carrito': carrito,
        'total': total
    }
    return render(request, "carrito.html",context)

