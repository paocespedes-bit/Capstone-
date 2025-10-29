from email.headerregistry import ContentTypeHeader
from .forms import CategoriaForm, PanelSIPForm, KitConstruccionForm, ImagenProductoForm
from store.models import PanelSIP, KitConstruccion, Categoria, imagenProducto,Inventario
from .models import Pedido,DetallePedido
from datetime import date
from .utils.boleta import generar_boleta_pdf
from decimal import Decimal, InvalidOperation
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import FileResponse, Http404
from django.utils import timezone
from django.db.models import Sum, F
from collections import Counter 

# !Views principales

def control(request):
    ahora = timezone.localtime(timezone.now())
    inicio_dia = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_dia = ahora.replace(hour=23, minute=59, second=59, microsecond=999999)

    pedidos_hoy = Pedido.objects.filter(fecha_pedido__range=(inicio_dia, fin_dia))

    # === Ventas por año ===
    ventas_anio = (
        Pedido.objects.annotate(anio=ExtractYear('fecha_pedido'))
        .values('anio')
        .annotate(total_anio=Sum('monto_total'))
        .order_by('anio')
    )
    labels_ventas_anio = [v['anio'] for v in ventas_anio]
    data_ventas_anio = [float(v['total_anio'] or 0) for v in ventas_anio]

    # === Ventas por mes ===
    year = ahora.year
    ventas_mes = (
        Pedido.objects.filter(fecha_pedido__year=year)
        .annotate(mes=F('fecha_pedido__month'))
        .values('mes')
        .annotate(total_mes=Sum('monto_total'))
        .order_by('mes')
    )
    labels_ventas_mes = [v['mes'] for v in ventas_mes]
    data_ventas_mes = [float(v['total_mes'] or 0) for v in ventas_mes]

    # === Ventas por día ===
    mes_actual = ahora.month
    ventas_dia = (
        Pedido.objects.filter(fecha_pedido__year=year, fecha_pedido__month=mes_actual)
        .annotate(dia=F('fecha_pedido__day'))
        .values('dia')
        .annotate(total_dia=Sum('monto_total'))
        .order_by('dia')
    )
    labels_ventas_dia = [v['dia'] for v in ventas_dia]
    data_ventas_dia = [float(v['total_dia'] or 0) for v in ventas_dia]

    # === Ingresos por tipo de producto ===
    ingresos_tipo = (
        DetallePedido.objects
        .values('content_type')
        .annotate(total_ingresos=Sum('subtotal'))
        .order_by('-total_ingresos')
    )

    labels_ingresos = []
    data_ingresos = []

    for item in ingresos_tipo:
        try:
            tipo = ContentType.objects.get_for_id(item['content_type']).model_class().__name__
        except Exception:
            tipo = "Desconocido"
        labels_ingresos.append(tipo)
        data_ingresos.append(float(item['total_ingresos'] or 0))

    # --- Ventas por tipo de producto + mes (nuevo) ---
    detalles = DetallePedido.objects.annotate(
        mes=ExtractMonth('pedido__fecha_pedido')
    ).values('mes', 'content_type').annotate(total_cantidad=Sum('cantidad'))

    tipos = {}
    meses = set()
    for det in detalles:
        tipo = ContentType.objects.get_for_id(det['content_type']).model_class().__name__
        meses.add(det['mes'])
        if tipo not in tipos:
            tipos[tipo] = {}
        tipos[tipo][det['mes']] = det['total_cantidad']

    meses = sorted(list(meses))
    labels_productos_mes = [f"Mes {m}" for m in meses]

    datasets_productos_mes = []
    colores = ['rgba(54,162,235,0.6)', 'rgba(255,99,132,0.6)', 'rgba(75,192,192,0.6)', 'rgba(255,206,86,0.6)']

    for i, (tipo, data_dict) in enumerate(tipos.items()):
        data = [data_dict.get(m, 0) for m in meses]
        datasets_productos_mes.append({
            'label': tipo,
            'data': data,
            'backgroundColor': colores[i % len(colores)]
        })

    context = {
        'pedidos_hoy': pedidos_hoy,
        'labels_ventas_anio': labels_ventas_anio,
        'data_ventas_anio': data_ventas_anio,
        'labels_ventas_mes': labels_ventas_mes,
        'data_ventas_mes': data_ventas_mes,
        'labels_ventas_dia': labels_ventas_dia,
        'data_ventas_dia': data_ventas_dia,
        'labels_ingresos': labels_ingresos,
        'data_ingresos': data_ingresos,
        'labels_productos_mes': labels_productos_mes,
        'datasets_productos_mes': datasets_productos_mes,
    }

    return render(request, 'home_control.html', context)

def safe_decimal(value):
    """Convierte string con coma o punto a Decimal, o None si no es válido."""
    if not value or value.strip() == "":
        return None
    try:
        return Decimal(value.replace(",", "."))
    except (InvalidOperation, AttributeError):
        return None

def stock(request):
    paneles = PanelSIP.objects.all()
    kits = KitConstruccion.objects.all()
    categorias = Categoria.objects.all()

    # Parámetros de orden y pestaña
    ordenar = request.GET.get("ordenar")
    direccion = request.GET.get("direccion")
    tab = request.GET.get("tab", "paneles")

    # --- FILTROS PERSONALIZADOS (solo paneles) ---
    tipo_obs = request.GET.get("tipo_obs")
    espesor = request.GET.get("espesor")
    largo = request.GET.get("largo")
    ancho = request.GET.get("ancho")

    # Aplicar filtros
    if tipo_obs and tipo_obs.strip() != "":
        paneles = paneles.filter(tipo_obs=tipo_obs)

    # Convertimos los valores a Decimal para los campos numéricos
    espesor_decimal = safe_decimal(espesor)
    largo_decimal = safe_decimal(largo)
    ancho_decimal = safe_decimal(ancho)

    if espesor_decimal is not None:
        paneles = paneles.filter(espesor=espesor_decimal)
    if largo_decimal is not None:
        paneles = paneles.filter(largo=largo_decimal)
    if ancho_decimal is not None:
        paneles = paneles.filter(ancho=ancho_decimal)

    # --- ORDENAMIENTO ---
    if ordenar:
        orden = f"-{ordenar}" if direccion == "desc" else ordenar

        if tab == "paneles":
            paneles = paneles.order_by(orden)
        elif tab == "kits":
            kits = kits.order_by(orden)
        elif tab == "cat":
            categorias = categorias.order_by(orden)

    # --- VALORES ÚNICOS PARA SELECTS ---
    tipo_obs_opciones = PanelSIP.objects.values_list("tipo_obs", flat=True).distinct()
    espesor_opciones = PanelSIP.objects.values_list("espesor", flat=True).distinct()
    largo_opciones = PanelSIP.objects.values_list("largo", flat=True).distinct()
    ancho_opciones = PanelSIP.objects.values_list("ancho", flat=True).distinct()

    context = {
        "paneles": paneles,
        "kits": kits,
        "categorias": categorias,
        "panel_form": PanelSIPForm(),
        "CategoriaForm": CategoriaForm(),
        "KitConstruccionForm": KitConstruccionForm(),
        "tipo_obs_opciones": tipo_obs_opciones,
        "espesor_opciones": espesor_opciones,
        "largo_opciones": largo_opciones,
        "ancho_opciones": ancho_opciones,
        # Guardamos los valores actuales para mantener selección
        "selected_tipo_obs": tipo_obs,
        "selected_espesor": espesor,
        "selected_largo": largo,
        "selected_ancho": ancho,
    }

    return render(request, "stock.html", context)

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

# !======================
# !CREAR 
# !======================

def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada correctamente.')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')

    # Siempre redirigimos a la pestaña de categorías
    return redirect(f"{reverse('stock')}?tab=cat")

def crear_panel(request):
    if request.method == 'POST':
        panel_form = PanelSIPForm(request.POST)
        if panel_form.is_valid():
            
            panel = panel_form.save(commit=False)
            panel.save()
            panel_form.save_m2m()
            
            # Obtener ContentType para PanelSIP
            panel_content_type = ContentType.objects.get_for_model(PanelSIP)
            
            modo_stock = request.POST.get('modo_stock')
            cantidad_str = request.POST.get('cantidad')
            
            cantidad_disponible = 0
            if modo_stock == 'stock' and cantidad_str:
                try:
                    cantidad_disponible = int(cantidad_str)
                except ValueError:
                    cantidad_disponible = 0
            
            Inventario.objects.create(
                # ASIGNACIÓN EXPLÍCITA DE LA GENERIC FOREIGN KEY
                content_type=panel_content_type,
                object_id=panel.id,
                disponible=cantidad_disponible,
                reservado=0,
                modo_stock=modo_stock if modo_stock else 'pedido'
            )

            messages.success(request, 'Panel SIP creado correctamente y se ha establecido su inventario.')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
        
        return redirect(f"{reverse('stock')}?tab=paneles")
    
    return redirect(f"{reverse('stock')}?tab=paneles")

def crear_kit(request):
    if request.method == 'POST':
        kit_form = KitConstruccionForm(request.POST)
        if kit_form.is_valid():
            
            kit = kit_form.save(commit=False)
            kit.save()
            kit_form.save_m2m()
            
            # Obtener ContentType para KitConstruccion
            kit_content_type = ContentType.objects.get_for_model(KitConstruccion)

            modo_stock = request.POST.get('modo_stock')
            cantidad_str = request.POST.get('cantidad')
            
            cantidad_disponible = 0
            if modo_stock == 'stock' and cantidad_str:
                try:
                    cantidad_disponible = int(cantidad_str)
                except ValueError:
                    cantidad_disponible = 0
            
            Inventario.objects.create(
                # ASIGNACIÓN EXPLÍCITA DE LA GENERIC FOREIGN KEY
                content_type=kit_content_type,
                object_id=kit.id,
                disponible=cantidad_disponible,
                reservado=0,
                modo_stock=modo_stock if modo_stock else 'pedido'
            )
            
            messages.success(request, 'Kit de construcción creado correctamente y se ha establecido su inventario.')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')

        
        return redirect(f"{reverse('stock')}?tab=kits")
    

    return redirect(f"{reverse('stock')}?tab=kits")

# !======================
# !SUBIR IMAGENES 
# !======================

def subir_imagenes_panel(request, panel_id):
    panel = get_object_or_404(PanelSIP, id=panel_id)

    if request.method == "POST":
        archivos = request.FILES.getlist('imagenes')
        errores = []

        for archivo in archivos:
            # Crear formulario individual para cada archivo
            form = ImagenProductoForm(files={'imagen': archivo})
            if form.is_valid():
                nueva_imagen = form.save(commit=False)
                nueva_imagen.content_type = ContentType.objects.get_for_model(panel)
                nueva_imagen.object_id = panel.id
                nueva_imagen.full_clean()  # ✅ Ejecuta validaciones del modelo también
                nueva_imagen.save()
            else:
                # Agregar error al listado para mostrarlo en la plantilla
                errores.append(f"{archivo.name}: {form.errors.get('imagen')[0]}")

        if errores:
            for err in errores:
                messages.error(request, err)
        else:
            messages.success(request, "Imágenes subidas correctamente.")

        return redirect('stock')

    return render(request, 'stock.html', {'panel': panel})

def subir_imagenes_kit(request, kit_id):
    kit = get_object_or_404(KitConstruccion, id=kit_id)

    if request.method == "POST":
        archivos = request.FILES.getlist('imagenes')
        errores = []

        for archivo in archivos:
            form = ImagenProductoForm(files={'imagen': archivo})
            if form.is_valid():
                nueva_imagen = form.save(commit=False)
                nueva_imagen.content_type = ContentType.objects.get_for_model(kit)
                nueva_imagen.object_id = kit.id
                nueva_imagen.full_clean()
                nueva_imagen.save()
            else:
                errores.append(f"{archivo.name}: {form.errors.get('imagen')[0]}")

        if errores:
            for err in errores:
                messages.error(request, err)
        else:
            messages.success(request, "Imágenes subidas correctamente.")

        return redirect('/stock/?tab=kits')

    return render(request, 'tabla_kits.html', {"kit": kit})

# !======================
# !ELIMINAR IMAGENES
# !======================

def eliminar_imagen_kit(request, imagen_id):
    imagen = get_object_or_404(imagenProducto, id=imagen_id)
    kit = imagen.producto  # Instancia real: PanelSIP o KitConstruccion

    if request.method == 'POST':
        imagen.delete()
        return redirect('/stock/?tab=kits')

def eliminar_imagen(request, imagen_id):
    imagen = get_object_or_404(imagenProducto, id=imagen_id)
    panel = imagen.producto  # Instancia real: PanelSIP o KitConstruccion

    if request.method == 'POST':
        imagen.delete()
        return redirect('stock')

# !======================
# !EDITAR
# !======================

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
        
        # Guardar relaciones Many-to-Many
        panel.categorias.set(request.POST.getlist('categorias'))

        # Actualizar Inventario
        inventario = panel.inventario.first() 
        
        if inventario:
            modo_stock = request.POST.get('modo_stock')
            cantidad_str = request.POST.get('cantidad')
            
            inventario.modo_stock = modo_stock if modo_stock else 'pedido'
            
            if inventario.modo_stock == 'stock' and cantidad_str:
                try:
                    inventario.disponible = int(cantidad_str) 
                except ValueError:
                    pass

            inventario.save()
        
        return redirect(f"{reverse('stock')}?tab=paneles")

    return redirect(f"{reverse('stock')}?tab=paneles") 

def editar_kit(request, pk):
    kit = get_object_or_404(KitConstruccion, pk=pk)
    
    if request.method == "POST":
        form = KitConstruccionForm(request.POST, instance=kit)
        if form.is_valid():
            form.save()
            
            # Actualizar Inventario
            inventario = kit.inventario.first()
            
            if inventario:
                modo_stock = request.POST.get('modo_stock')
                cantidad_str = request.POST.get('cantidad')
                
                inventario.modo_stock = modo_stock if modo_stock else 'pedido'
                
                if inventario.modo_stock == 'stock' and cantidad_str:
                    try:
                        inventario.disponible = int(cantidad_str)
                    except ValueError:
                        pass
                
                inventario.save()
                
            return redirect(f"{reverse('stock')}?tab=kits")
        
        return redirect(f"{reverse('stock')}?tab=kits")
        
    return redirect(f"{reverse('stock')}?tab=kits")

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

# !======================
# !ELIMINAR
# !======================

# Eliminar categoría
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == "POST":
        nombre = categoria.nombre
        categoria.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada correctamente.')

    # Redirigimos siempre a la pestaña de categorías
    return redirect(f"{reverse('stock')}?tab=cat")

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


# !======================
# !BOLETAS
# !======================

def descargar_boleta(request, pedido_id):
    try:
        pedido = Pedido.objects.get(id=pedido_id)
    except Pedido.DoesNotExist:
        raise Http404("El pedido no existe")

    detalles = DetallePedido.objects.filter(pedido=pedido)
    pdf_buffer = generar_boleta_pdf(pedido, detalles)
    filename = f"boleta_pedido_{pedido.id}.pdf"

    return FileResponse(pdf_buffer, as_attachment=True, filename=filename)

def save(self,*args, **kwargs):
    if not self.nombre_producto and self.producto:
        self.nombre_producto = getattr(self.producto, 'nombre', 'Producto Desconocido')
    self.subtotal = self.precio_unitario * self.cantidad
    super().save(*args,**kwargs)
    self.pedido.actualizar_monto_total()


# !======================
# !ESTADO DE PEDIDO----DISEÑO
# !======================


def cambiar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == "POST":
        nuevo_estado = request.POST.get("nuevo_estado")
        if nuevo_estado in dict(Pedido.ESTADOS).keys():
            pedido.estado = nuevo_estado
            pedido.save()
            pedido.actualizar_stock_por_estado()
            messages.success(request, f"Estado del pedido #{pedido.id} actualizado a {pedido.get_estado_display()}.")
        else:
            messages.error(request, "Estado no válido.")
    
    return redirect(request.META.get("HTTP_REFERER", "pedidos_list"))

