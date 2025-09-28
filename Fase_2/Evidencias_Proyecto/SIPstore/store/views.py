from django.shortcuts import render, get_object_or_404
from .models import PanelSIP, KitConstruccion

# ==========================================
# Views para Paneles SIP
# ==========================================
def paneles(request):
    paneles = PanelSIP.objects.all()

    # --------------------
    # Filtros
    # --------------------
    tipo_obs = request.GET.get('tipo_obs')
    if tipo_obs:
        paneles = paneles.filter(tipo_obs=tipo_obs)

    espesor = request.GET.get('espesor')
    if espesor:
        try:
            espesor_val = float(espesor)
            paneles = paneles.filter(espesor=espesor_val)
        except ValueError:
            pass

    madera_union = request.GET.get('madera_union')
    if madera_union:
        paneles = paneles.filter(madera_union=madera_union)

    precio_max = request.GET.get('precio_max')
    if precio_max:
        try:
            precio_val = float(precio_max)
            paneles = paneles.filter(precio__lte=precio_val)
        except ValueError:
            pass

    context = {
        'paneles': paneles
    }
    return render(request, 'paneles.html', context)


def paneles_detail(request, pk):
    panel = get_object_or_404(PanelSIP, pk=pk)
    context = {'panel': panel}
    return render(request, 'paneles_detail.html', context)


# ==========================================
# Views para Kits de Construcción
# ==========================================
def kits(request):
    kits = KitConstruccion.objects.all()

    # --------------------
    # Filtros (ejemplo: podrías agregar filtros similares)
    # --------------------
    # Por ahora solo filtraremos por precio máximo
    precio_max = request.GET.get('precio_max')
    if precio_max:
        try:
            precio_val = float(precio_max)
            kits = kits.filter(precio__lte=precio_val)
        except ValueError:
            pass

    context = {'kits': kits}
    return render(request, "kits.html", context)


def kit_detail(request, pk):
    kit = get_object_or_404(KitConstruccion, pk=pk)
    context = {'kit': kit}
    return render(request, 'kit_detail.html', context)
