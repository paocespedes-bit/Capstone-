from django.shortcuts import render
from store.models import PanelSIP, KitConstruccion, Categoria


#! Aqui se agregan las views (templates).
def control(request):
    return render(request, 'home_control.html')

def stock(request):

    order = request.GET.get("order", "").strip()    # Obtener ordenamiento

    paneles = PanelSIP.objects.all()
    kits = KitConstruccion.objects.all()
    categorias = Categoria.objects.all()

    # Orden dinámico
    order_map_paneles_string = {
        "id_asc": "id",
        "id_desc": "-id",
        "cantidad_asc": "cantidad",      # si existe
        "cantidad_desc": "-cantidad",    # si existe
        "nombre_asc": "nombre",
        "nombre_desc": "-nombre",
        "precio_asc": "precio",
        "precio_desc": "-precio",
        "oferta_asc": "ofertas",
        "oferta_desc": "-ofertas",
        "tipo_obs_asc": "tipo_obs",
        "tipo_obs_desc": "-tipo_obs",
        "espesor_asc": "espesor",
        "espesor_desc": "-espesor",
        "largo_asc": "largo",
        "largo_desc": "-largo",
        "ancho_asc": "ancho",
        "ancho_desc": "-ancho",
    }

    if order in order_map_paneles_string:
        paneles = paneles.order_by(order_map_paneles_string[order])

    context = {
        "paneles": paneles,
        "order": order,
        'kits': kits,
        'categorias': categorias,
    }
    return render(request, 'stock.html', context)


