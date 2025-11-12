from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.db.models import Avg
from .models import Calificacion
from .forms import CalificacionForm

def calificar_producto(request, app_label, model_name, producto_id):
    content_type = get_object_or_404(ContentType, app_label=app_label, model=model_name)
    producto = content_type.get_object_for_this_type(id=producto_id)

    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.content_type = content_type
            calificacion.object_id = producto_id
            calificacion.usuario = request.user if request.user.is_authenticated else None
            calificacion.save()
            messages.success(request, "Gracias por tu calificación.")

            if model_name.lower() == 'panelsip':
                return redirect('paneles_detail', pk=producto_id)
            elif model_name.lower() == 'kitconstruccion':
                return redirect('kit_detail', pk=producto_id)
            else:
                return redirect('/')
    else:
        form = CalificacionForm()

    calificaciones = Calificacion.objects.filter(
        content_type=content_type, object_id=producto_id
    )
    promedio = calificaciones.aggregate(Avg('estrellas'))['estrellas__avg'] or 0

    return render(request, 'coment/calificar.html', {
        'producto': producto,
        'form': form,
        'promedio': round(promedio, 1),
        'calificaciones': calificaciones,
    })
