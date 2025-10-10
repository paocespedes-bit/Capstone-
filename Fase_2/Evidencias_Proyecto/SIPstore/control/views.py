from email.headerregistry import ContentTypeHeader
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CategoriaForm, PanelSIPForm, KitConstruccionForm, ImagenProductoForm
from store.models import PanelSIP, KitConstruccion, Categoria, imagenProducto
from .models import Pedido,DetallePedido
from django.utils import timezone
from django.db.models import Sum, F
from collections import Counter 
from django.db.models.functions import ExtractYear

# Views principales
def control(request):
    ahora = timezone.localtime(timezone.now())
    inicio_dia = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_dia = ahora.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Pedidos de hoy
    pedidos_hoy = Pedido.objects.filter(fecha_pedido__range=(inicio_dia, fin_dia))

    # Ventas por año
    ventas_anio = Pedido.objects.annotate(anio=ExtractYear('fecha_pedido'))\
        .values('anio')\
        .annotate(total_anio=Sum('monto_total'))\
        .order_by('anio')

    labels_ventas_anio = [v['anio'] for v in ventas_anio]
    data_ventas_anio = [float(v['total_anio']) for v in ventas_anio]

    # Ventas por mes
    year = ahora.year
    ventas_mes = Pedido.objects.filter(fecha_pedido__year=year)\
        .annotate(mes=F('fecha_pedido__month'))\
        .values('mes')\
        .annotate(total_mes=Sum('monto_total'))\
        .order_by('mes')

    labels_ventas_mes = [v['mes'] for v in ventas_mes]
    data_ventas_mes = [float(v['total_mes']) for v in ventas_mes]

    # TOP 3 productos
    detalles = DetallePedido.objects.all()
    productos_cantidad = Counter()
    for detalle in detalles:
        productos_cantidad[detalle.producto.nombre] += detalle.cantidad

    top_productos = productos_cantidad.most_common(3)
    labels_top_productos = [p[0] for p in top_productos]
    data_top_productos = [p[1] for p in top_productos]

    # Ventas por día
    mes_actual = ahora.month
    ventas_dia = Pedido.objects.filter(fecha_pedido__year=year, fecha_pedido__month=mes_actual)\
        .annotate(dia=F('fecha_pedido__day'))\
        .values('dia')\
        .annotate(total_dia=Sum('monto_total'))\
        .order_by('dia')

    labels_ventas_dia = [v['dia'] for v in ventas_dia]
    data_ventas_dia = [float(v['total_dia']) for v in ventas_dia]

    context = {
        'pedidos_hoy': pedidos_hoy,
        'labels_ventas_anio': labels_ventas_anio,
        'data_ventas_anio': data_ventas_anio,
        'labels_ventas_mes': labels_ventas_mes, 
        'data_ventas_mes': data_ventas_mes,
        'labels_top_productos': labels_top_productos,
        'data_top_productos': data_top_productos,
        'labels_ventas_dia': labels_ventas_dia,
        'data_ventas_dia': data_ventas_dia,
    }

    return render(request, 'home_control.html', context)


def subir_imagenes_panel(request, panel_id):
    panel = get_object_or_404(PanelSIP, id=panel_id)

    if request.method == "POST":
        for imagen in request.FILES.getlist('imagenes'):
            imagenProducto.objects.create(
                imagen=imagen,
                content_type=ContentType.objects.get_for_model(panel),
                object_id=panel.id
            )
        return redirect('stock')  

    return render(request, 'stock.html', {'panel': panel})

def eliminar_imagen(request, imagen_id):
    imagen = get_object_or_404(imagenProducto, id=imagen_id)
    panel = imagen.producto  # Instancia real: PanelSIP o KitConstruccion

    if request.method == 'POST':
        imagen.delete()
        return redirect('stock')
    
def subir_imagenes_kit(request, kit_id):
    kit = get_object_or_404(KitConstruccion, id=kit_id)

    if request.method == "POST":
        for imagen in request.FILES.getlist('imagenes'):
            imagenProducto.objects.create(
                imagen=imagen,
                content_type=ContentType.objects.get_for_model(kit),
                object_id=kit.id
            )
        return redirect('/stock/?tab=kits') 

    return render(request, 'tabla_kits.html', {"kit": kit})

def eliminar_imagen_kit(request, imagen_id):
    imagen = get_object_or_404(imagenProducto, id=imagen_id)
    kit = imagen.producto  # Instancia real: PanelSIP o KitConstruccion

    if request.method == 'POST':
        imagen.delete()
        return redirect('/stock/?tab=kits')

def stock(request):
    paneles = PanelSIP.objects.all()
    kits = KitConstruccion.objects.all()
    categorias = Categoria.objects.all()
    ordenar = request.GET.get("ordenar")
    direccion = request.GET.get("direccion")

    if ordenar:
        if direccion == "desc":
            paneles = paneles.order_by(f"-{ordenar}")
        else:
            paneles = paneles.order_by(ordenar)

    if ordenar:
        if direccion == "desc":
            kits = kits.order_by(f"-{ordenar}")
        else:
            kits = kits.order_by(ordenar)

    context = {
        'paneles': paneles,
        'kits': kits,
        'categorias': categorias,
        'panel_form': PanelSIPForm(),  
        'CategoriaForm': CategoriaForm(),
        'KitConstruccionForm': KitConstruccionForm(),
    }
    return render(request, 'stock.html', context)


def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada correctamente.')
            return redirect('/stock/?tab=cat')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = CategoriaForm()
    return render(request, 'tabla_categoria.html', {'form': form, 'titulo': 'Nueva Categoría'})

def crear_panel(request):
    if request.method == 'POST':
        panel_form = PanelSIPForm(request.POST)
        if panel_form.is_valid():
            panel_form.save()
            messages.success(request, 'Panel SIP creado correctamente.')
            return redirect('stock')
    else:
        panel_form = PanelSIPForm()

    return render(request, 'stock.html', {
        'panel_form': panel_form,
        'paneles': PanelSIP.objects.all(),
        'categorias': Categoria.objects.all()
    })

def crear_kit(request):
    if request.method == 'POST':
        kit_form = KitConstruccionForm(request.POST)

        if kit_form.is_valid():
            kit_form.save()

            messages.success(request, 'Kit de construcción creado correctamente.')
            return redirect('/stock/?tab=kits')
    else:
        kit_form = KitConstruccionForm()

    return render(request, 'formularios.html', {
        'form': kit_form,
        'titulo': 'Nuevo Kit de Construcción'
    })
    
    
# Eliminar categoría
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        nombre = categoria.nombre
        categoria.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada correctamente.')
        return redirect('/stock/?tab=cat')
    return redirect('/stock/?tab=cat')

# Eliminar panel
def eliminar_panel(request, pk):
    panel = get_object_or_404(PanelSIP, pk=pk)
    if request.method == "POST":
        panel.delete()
        messages.success(request, 'Panel SIP eliminado correctamente.')
        return redirect('stock')
    return redirect('stock')

# Eliminar kit
def eliminar_kit(request, pk):
    kit = get_object_or_404(KitConstruccion, pk=pk)
    if request.method == "POST":
        kit.delete()
        messages.success(request, 'Kit de construcción eliminado correctamente.')
        return redirect('/stock/?tab=kits')
    return redirect('/stock/?tab=kits')

def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('/stock/?tab=cat')  # usa la vista que carga stock.html
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'editar_categoria.html', {'form': form, 'categoria': categoria})

def editar_panel(request, pk):
    panel = get_object_or_404(PanelSIP, pk=pk)

    if request.method == 'POST':
        # Guardar datos del panel
        panel.nombre = request.POST.get('nombre')
        panel.precio = request.POST.get('precio')
        panel.descripcion = request.POST.get('descripcion')
        panel.tipo_obs = request.POST.get('tipo_obs')
        panel.madera_union = request.POST.get('madera_union')
        panel.espesor = request.POST.get('espesor')
        panel.largo = request.POST.get('largo')
        panel.ancho = request.POST.get('ancho')
        panel.save()
        panel.categorias.set(request.POST.getlist('categorias'))

        return redirect('stock')

    return render(request, 'stock.html', {
        'panel_form': None,  # No necesitamos el panel_form aquí
        'paneles': PanelSIP.objects.all(),
        'categorias': Categoria.objects.all(),
    })

def editar_kit(request, pk):
    kit = get_object_or_404(KitConstruccion, pk=pk)
    if request.method == "POST":
        form = KitConstruccionForm(request.POST, instance=kit)
        if form.is_valid():
            form.save()
            # Redirige al inventario con query param para la pestaña de kits
            return redirect(f"{reverse('stock')}?tab=kits")
    else:
        form = KitConstruccionForm(instance=kit)
    return render(request, "editar_kit.html", {"form": form})


def pedidos(request):
    pedidos = Pedido.objects.all()
    ordenar = request.GET.get("ordenar")
    direccion = request.GET.get("direccion")

    if ordenar:
        if direccion == "desc":
            pedidos = pedidos.order_by(f"-{ordenar}")
        else:
            pedidos = pedidos.order_by(ordenar)

    context = {
        'pedidos' : pedidos   
    }
    return render(request,'pedidos.html',context)

def pedido_detail(request, pk):
    pedidos = get_object_or_404(Pedido, pk=pk)
    detalles = DetallePedido.objects.filter(pedido=pedidos)  
    context ={
        'pedido': pedidos,
        'detalles': detalles
    }
    return render(request, 'pedido_detail.html', context)



