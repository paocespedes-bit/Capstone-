from django.shortcuts import render
from store.models import PanelSIP, Categoria
from django.db.models import Q

def quote(request):
    modulos = {
        # !Ojo con las categorias tienen que tener estos mismos nombres
        'piso': 'Piso',
        'cielo': 'Cielo',
        'muros_int': 'Muros Internos',
        'muros_ext': 'Muros Externos', 
    }

    contexto = {}

    for key, nombre_categoria in modulos.items():
        categoria = Categoria.objects.filter(nombre__iexact=nombre_categoria).first()

        if categoria:
            paneles = (
                PanelSIP.objects.filter(categorias__id=categoria.id)
                .filter(
                    Q(inventario__modo_stock='stock', inventario__disponible__gt=0)
                    | Q(inventario__modo_stock='pedido')
                )
                .distinct()[:5]
            )
            #!Despues borrar
            print(f"==============================")
            print(f"Categoría buscada: {nombre_categoria}")
            print(f"✅ Categoría encontrada: {categoria.nombre} (id={categoria.id})")
            print(f"➡️ Paneles con esa categoría: {PanelSIP.objects.filter(categorias__id=categoria.id).count()}")
            print(f"➡️ Paneles con inventario válido: {paneles.count()}")
            print(f"==============================")
            #!======================================================
            contexto[key] = paneles
        else:
            print(f"Categoría buscada: {nombre_categoria} ❌ No se encontró la categoría.") #!Despues borrar
            contexto[key] = []

    return render(request, 'quote.html', contexto)
