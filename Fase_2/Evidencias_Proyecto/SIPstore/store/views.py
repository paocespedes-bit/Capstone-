from django.db.models import Min, Max
from django.shortcuts import render
from .models import PanelSIP, KitConstruccion

#! Aqui se agregan las views (templates).
def paneles(request):
 # Filtros para paneles
    search = request.GET.get('search', '').strip()

    tipo_obs_filtro = request.GET.get('tipo_obs', '').strip()
    Espesor_OSB_filtro = request.GET.get('espesor', '').strip()
    madera_union_filtro = request.GET.get('madera_union', '').strip()

    precio_max = request.GET.get('precio_max', '').strip()

    paneles_sip = PanelSIP.objects.all()
    # Filtros para paneles por busqueda de caracteres
    if search:
        paneles_sip = paneles_sip.filter(tipo_obs__icontains=search)
    # Filtros para paneles por select opcional de tipo de filtro
    if tipo_obs_filtro:
        paneles_sip = paneles_sip.filter(tipo_obs=tipo_obs_filtro)
    # Filtros para paneles por select opcional de espesor del OSB
    if Espesor_OSB_filtro:
        paneles_sip = paneles_sip.filter(espesor=Espesor_OSB_filtro)
    # Filtros para paneles por select opcional de Madera de union
    if madera_union_filtro:
        paneles_sip = paneles_sip.filter(madera_union=madera_union_filtro)
    # Filtros para paneles por precio
    MIN_PRECIO = 0
    paneles_sip = paneles_sip.filter(precio__gte=MIN_PRECIO)

    if precio_max:
        try:
            paneles_sip = paneles_sip.filter(precio__lte=float(precio_max))
        except ValueError:
            pass  # ignora si el valor no es numérico

    tipos_obs = PanelSIP.objects.values_list('tipo_obs', flat=True).distinct()
    espesores = PanelSIP.objects.values_list('espesor', flat=True).distinct()
    maderas = PanelSIP.objects.values_list('madera_union', flat=True).distinct()
    
    context = {
        'paneles': paneles_sip,
        'tipos_obs': tipos_obs,
        'espesores': espesores,
        'maderas': maderas,
        'search': search,
        'tipo_obs_filtro': tipo_obs_filtro,
        'Espesor_OSB_filtro': Espesor_OSB_filtro,
        'madera_union_filtro': madera_union_filtro,
        'precio_min': MIN_PRECIO,
        'precio_max': precio_max,
    }
    return render(request, 'paneles.html', context)

def kits(request):
    kits = KitConstruccion.objects.all()
    context = {
        
        'kits': kits
    }
    return render(request, "kits.html",context)





