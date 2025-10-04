from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CategoriaForm, PanelSIPForm, KitConstruccionForm
from store.models import PanelSIP, KitConstruccion, Categoria

# Views principales
def control(request):
    return render(request, 'home_control.html')


def stock(request):
    paneles = PanelSIP.objects.all()
    kits = KitConstruccion.objects.all()
    categorias = Categoria.objects.all()

    context = {
        'paneles': paneles,
        'kits': kits,
        'categorias': categorias,
        'CategoriaForm': CategoriaForm(),
        'PanelSIPForm': PanelSIPForm(),
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
    return render(request, 'formularios.html', {'form': form, 'titulo': 'Nueva Categoría'})

def crear_panel(request):
    if request.method == 'POST':
        panel_form = PanelSIPForm(request.POST)

        if panel_form.is_valid():
            panel_form.save()

            messages.success(request, 'Panel SIP creado correctamente.')
            return redirect('stock')
    else:
        panel_form = PanelSIPForm()
        

    return render(request, 'formularios.html', {
        'form': panel_form,
        'titulo': 'Nuevo Panel SIP'
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
        categoria.delete()
        messages.success(request, 'Categoría eliminada correctamente.')
        return redirect('stock')
    return redirect('stock')  # por seguridad, si acceden por GET

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
