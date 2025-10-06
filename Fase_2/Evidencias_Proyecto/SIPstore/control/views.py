from email.headerregistry import ContentTypeHeader
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CategoriaForm, PanelSIPForm, KitConstruccionForm, ImagenProductoForm
from store.models import PanelSIP, KitConstruccion, Categoria, imagenProducto

# Views principales
def control(request):
    return render(request, 'home_control.html')

def subir_imagenes_panel(request, panel_id):
    panel = get_object_or_404(PanelSIP, id=panel_id)

    if request.method == "POST":
        for imagen in request.FILES.getlist('imagenes'):
            imagenProducto.objects.create(
                imagen=imagen,
                content_type=ContentType.objects.get_for_model(panel),
                object_id=panel.id
            )
        return redirect('stock')  # o a la página que quieras

    return render(request, 'stock.html', {'panel': panel})

def eliminar_imagen(request, imagen_id):
    imagen = get_object_or_404(imagenProducto, id=imagen_id)
    panel = imagen.producto  # Instancia real: PanelSIP o KitConstruccion

    if request.method == 'POST':
        imagen.delete()
        return redirect('stock')


def stock(request):
    paneles = PanelSIP.objects.all()
    kits = KitConstruccion.objects.all()
    categorias = Categoria.objects.all()

    context = {
        'paneles': paneles,
        'kits': kits,
        'categorias': categorias,
        'panel_form': PanelSIPForm(),  # 🔹 aquí el nombre coincide con el template
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
            return redirect('stock')
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
            return redirect('stock')
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
        return redirect('stock')
    return redirect('stock')

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
        return redirect('stock')
    return redirect('stock')

def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('stock')  # usa la vista que carga stock.html
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'editar_categoria.html', {'form': form, 'categoria': categoria})

def editar_panel(request, panel_id):
    panel = get_object_or_404(PanelSIP, id=panel_id)

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
            return redirect("stock")  # Redirige al inventario
    else:
        form = KitConstruccionForm(instance=kit)
    return render(request, "editar_kit.html", {"form": form})