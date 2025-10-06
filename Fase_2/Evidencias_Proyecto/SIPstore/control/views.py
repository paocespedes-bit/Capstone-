from email.headerregistry import ContentTypeHeader
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CategoriaForm, PanelSIPForm, KitConstruccionForm, ImagenFormSet
from store.models import PanelSIP, KitConstruccion, Categoria, imagenProducto

# Views principales
def control(request):
    return render(request, 'home_control.html')


def stock(request):
    paneles = PanelSIP.objects.all()
    kits = KitConstruccion.objects.all()
    categorias = Categoria.objects.all()
    form_kit = KitConstruccionForm()

    context = {
        'paneles': paneles,
        'kits': kits,
        'categorias': categorias,
        'CategoriaForm': CategoriaForm(),
        'PanelSIPForm': PanelSIPForm(),
        'KitConstruccionForm': KitConstruccionForm(),
        'form_kit': form_kit,
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
        imagen_formset = ImagenFormSet(request.POST, request.FILES)

        if panel_form.is_valid() and imagen_formset.is_valid():
            panel = panel_form.save()

            # Guardar imágenes asociadas
            for form in imagen_formset:
                imagen = form.cleaned_data.get('imagen')
                if imagen:
                    imagenProducto.objects.create(
                        imagen=imagen,
                        content_type=ContentType.objects.get_for_model(panel),
                        object_id=panel.id
                    )

            messages.success(request, 'Panel SIP creado correctamente.')
            return redirect('stock')

    else:
        panel_form = PanelSIPForm()
        imagen_formset = ImagenFormSet()  # ✅ 5 inputs vacíos garantizados

    return render(request, 'stock.html', {
        'panel_form': panel_form,
        'ImagenFormSet': imagen_formset,
        'paneles': PanelSIP.objects.all(),
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


def editar_panel(request, pk):
    panel = get_object_or_404(PanelSIP, pk=pk)

    if request.method == 'POST':
        form = PanelSIPForm(request.POST, instance=panel)
        if form.is_valid():
            form.save()
            return redirect('stock')  # Ajusta al nombre de la vista que renderiza stock.html
    else:
        form = PanelSIPForm(instance=panel)

    return render(request, 'editar_panel.html', {'form': form, 'panel': panel})

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