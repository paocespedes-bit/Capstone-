from django.db.models import Min, Max
from django.shortcuts import render
from .models import PanelSIP, KitConstruccion

#! Aqui se agregan las views (templates).
def paneles(request):
 # Filtros para paneles
    tipo_obs_filtro = request.GET.get('tipo_obs', '').strip()
    espesor_OSB_filtro = request.GET.get('espesor', '').strip()
    madera_union_filtro = request.GET.get('madera_union', '').strip()
    precios = PanelSIP.objects.aggregate(precio_min=Min('precio'), precio_max= Max('precio'))
    
    precio_min = precios['precio_min']
    precio_max = precios['precio_max']

    paneles = PanelSIP.objects.all()
    # Filtros para paneles por select opcional de tipo de filtro
    if tipo_obs_filtro:
        paneles = paneles.filter(tipo_obs=tipo_obs_filtro)
    # Filtros para paneles por select opcional de espesor del OSB
    if espesor_OSB_filtro:
        paneles = paneles.filter(espesor=espesor_OSB_filtro)
    # Filtros para paneles por select opcional de Madera de union
    if madera_union_filtro:
        paneles = paneles.filter(madera_union=madera_union_filtro)
    # Filtros para paneles por precio
    MIN_PRECIO = precio_min 
    paneles = paneles.filter(precio__gte=MIN_PRECIO)

    if precio_max:
        try:
            paneles = paneles.filter(precio__lte=float(precio_max))
        except ValueError:
            pass  # ignora si el valor no es numérico

    tipos_obs = PanelSIP.objects.values_list('tipo_obs', flat=True).distinct()
    espesores = PanelSIP.objects.values_list('espesor', flat=True).distinct()
    maderas = PanelSIP.objects.values_list('madera_union', flat=True).distinct()
    
    context = {
        'paneles': paneles,
        'tipos_obs': tipos_obs,
        'espesores': espesores,
        'maderas': maderas,
        'tipo_obs_filtro': tipo_obs_filtro,
        'espesor_OSB_filtro': espesor_OSB_filtro,
        'madera_union_filtro': madera_union_filtro,
        'precio_min': MIN_PRECIO,
        'precio_max': precio_max,
    }
    return render(request, 'paneles.html', context)

def kits(request):
    m2_filtro = request.GET.get('m2','').strip()
    dormitorios_filtro = request.GET.get('dormitorios','').strip()
    banos_filtro = request.GET.get('banos','').strip()
    precios = KitConstruccion.objects.aggregate(precio_min=Min('precio'), precio_max=Max('precio'))
    
    precio_min = precios['precio_min']
    precio_max = precios['precio_max']
    
    
    
    kits = KitConstruccion.objects.all()
    
    if m2_filtro:
        m2_filtro = float(m2_filtro.replace(',', '.'))
        kits = kits.filter(m2=m2_filtro)
    if dormitorios_filtro:
        kits = kits.filter(dormitorios=dormitorios_filtro)
    if banos_filtro:
        kits = kits.filter(banos=banos_filtro)    
    
    kits = kits.filter(precio__gte=precio_min)
    
    if precio_max:
        try:
            kits = kits.filter(precio__lte=float(precio_max))
        except ValueError:
            pass
    
    m2 = KitConstruccion.objects.values_list('m2',flat=True).distinct()
    dormitorios = KitConstruccion.objects.values_list('dormitorios',flat=True).distinct()
    banos = KitConstruccion.objects.values_list('banos',flat=True).distinct()
    
    context = {
        'kits': kits,
        'm2' : m2,
        'dormitorios' : dormitorios,
        'banos' : banos,
        'm2_filtro' : m2_filtro,
        'dormitorios_filtro' : dormitorios_filtro,
        'banos_filtro' : banos_filtro,
        'precios' : precios,
        'precio_min' : precio_min,
        'precio_max' : precio_max,
    }
    return render(request, "kits.html",context)





