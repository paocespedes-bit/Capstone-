from django.db.models import Min, Max, Avg
from django.shortcuts import render, get_object_or_404
from .models import PanelSIP, KitConstruccion
from django.core.paginator import Paginator
from coment.models import Calificacion

#! Aqui se agregan las views (templates).
def paneles(request):
    # filtros desde GET
    tipo_obs_filtro = request.GET.get('tipo_obs', '').strip()
    espesor_OSB_filtro = request.GET.get('espesor_OSB', '').strip()
    madera_union_filtro = request.GET.get('madera_union', '').strip()

    # extremos del dataset
    precios = PanelSIP.objects.aggregate(precio_min=Min('precio'), precio_max=Max('precio'))
    precio_min = precios['precio_min'] or 0
    precio_max_dataset = precios['precio_max'] or 0

    paneles_sip = PanelSIP.objects.all().order_by('nombre')

    # filtros no relacionados con precio
    if tipo_obs_filtro:
        paneles_sip = paneles_sip.filter(tipo_obs=tipo_obs_filtro)

    if espesor_OSB_filtro:
        paneles_sip = paneles_sip.filter(espesor=espesor_OSB_filtro)

    if madera_union_filtro:
        paneles_sip = paneles_sip.filter(madera_union=madera_union_filtro)

    # filtro mínimo de precio
    paneles_sip = paneles_sip.filter(precio__gte=precio_min)

    # filtro máximo de precio (slider)
    precio_max_selected = request.GET.get('precio_max')
    if precio_max_selected:
        try:
            precio_max_val = float(precio_max_selected)
            paneles_sip = paneles_sip.filter(precio__lte=precio_max_val)
            precio_max_selected = int(precio_max_val)
        except (ValueError, TypeError):
            precio_max_selected = precio_max_dataset
    else:
        precio_max_selected = precio_max_dataset

    # selects
    tipos_obs = PanelSIP.objects.values_list('tipo_obs', flat=True).distinct()
    espesores = PanelSIP.objects.values_list('espesor', flat=True).distinct()
    maderas = PanelSIP.objects.values_list('madera_union', flat=True).distinct()

    # paginación
    paginator = Paginator(paneles_sip, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 🔥 AGREGAR PROMEDIO A CADA PANEL
    for p in page_obj:
        p.promedio = Calificacion.objects.filter(
            content_type__model='panelsip',
            object_id=p.id
        ).aggregate(Avg('estrellas'))['estrellas__avg']

    context = {
        'paneles': page_obj,
        'tipos_obs': tipos_obs,
        'espesores': espesores,
        'maderas': maderas,
        'tipo_obs_filtro': tipo_obs_filtro,
        'espesor_OSB_filtro': espesor_OSB_filtro,
        'madera_union_filtro': madera_union_filtro,
        'precio_min': precio_min,
        'precio_max': precio_max_dataset,
        'precio_max_selected': precio_max_selected,
    }

    return render(request, 'paneles.html', context)

def kits(request):
    # filtros desde GET
    m2_filtro = request.GET.get('m2', '').strip()
    dormitorios_filtro = request.GET.get('dormitorios', '').strip()
    banos_filtro = request.GET.get('banos', '').strip()

    # extremos de precios
    precios = KitConstruccion.objects.aggregate(precio_min=Min('precio'), precio_max=Max('precio'))
    precio_min = precios['precio_min'] or 0
    precio_max_dataset = precios['precio_max'] or 0

    kits = KitConstruccion.objects.all().order_by('nombre')

    # filtros
    if m2_filtro:
        try:
            m2_f = float(m2_filtro.replace(',', '.'))
            kits = kits.filter(m2=m2_f)
        except ValueError:
            pass

    if dormitorios_filtro:
        kits = kits.filter(dormitorios=dormitorios_filtro)

    if banos_filtro:
        kits = kits.filter(banos=banos_filtro)

    # precio mínimo
    kits = kits.filter(precio__gte=precio_min)

    # precio máximo (slider)
    precio_max_selected = request.GET.get('precio_max')
    if precio_max_selected:
        try:
            precio_max_val = float(precio_max_selected)
            kits = kits.filter(precio__lte=precio_max_val)
            precio_max_selected = int(precio_max_val)
        except (ValueError, TypeError):
            precio_max_selected = precio_max_dataset
    else:
        precio_max_selected = precio_max_dataset

    # selects
    m2 = KitConstruccion.objects.values_list('m2', flat=True).distinct()
    dormitorios = KitConstruccion.objects.values_list('dormitorios', flat=True).distinct()
    banos = KitConstruccion.objects.values_list('banos', flat=True).distinct()

    # paginación
    paginator = Paginator(kits, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 🔥 AGREGAR PROMEDIO A CADA KIT
    for k in page_obj:
        k.promedio = Calificacion.objects.filter(
            content_type__model='kitconstruccion',
            object_id=k.id
        ).aggregate(Avg('estrellas'))['estrellas__avg']

    context = {
        'kits': page_obj,
        'm2': m2,
        'dormitorios': dormitorios,
        'banos': banos,
        'm2_filtro': m2_filtro,
        'dormitorios_filtro': dormitorios_filtro,
        'banos_filtro': banos_filtro,
        'precio_min': precio_min,
        'precio_max': precio_max_dataset,
        'precio_max_selected': precio_max_selected,
    }

    return render(request, "kits.html", context)

def kit_detail(request, pk):
    kit = get_object_or_404(KitConstruccion, pk=pk)
    calificaciones = Calificacion.objects.filter(
        content_type__model='kitconstruccion',
        object_id=kit.id
    ).select_related('usuario').order_by('-fecha')

    promedio = calificaciones.aggregate(promedio=Avg('estrellas'))['promedio']

    return render(request, 'kit_detail.html', {
        'kit': kit,
        'calificaciones': calificaciones,
        'promedio': promedio,
    })

def paneles_detail(request, pk):
    panel = get_object_or_404(PanelSIP, pk=pk)

    calificaciones = Calificacion.objects.filter(
        content_type__model='panelsip',
        object_id=panel.id
    ).select_related('usuario').order_by('-fecha')

    promedio = calificaciones.aggregate(promedio=Avg('estrellas'))['promedio']

    return render(request, 'paneles_detail.html', {
        'panel': panel,
        'calificaciones': calificaciones,
        'promedio': promedio,
    })


