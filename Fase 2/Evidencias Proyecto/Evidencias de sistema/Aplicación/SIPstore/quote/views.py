from django.shortcuts import render
from store.models import PanelSIP, Categoria
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

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
            
    request.session.flush()
    return render(request, 'quote.html', contexto)


@csrf_exempt
def save_form(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        module = data.get("module")
        form_data = data.get("data")
        
        if not module or not form_data:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
        
        session_forms = request.session.get("quote_forms", {})
        if module not in session_forms:
            session_forms[module] = []
        session_forms[module].append(form_data)

        request.session["quote_forms"] = session_forms
        request.session.modified = True   
        
        return JsonResponse({"message": "Formulario guardado temporalmente"})
    

@csrf_exempt
def calcular_materiales(request):
    if request.method == "POST":
        quote_data = request.session.get("quote_forms", {})
        if not quote_data:
            return JsonResponse({"html": "<p class='text-center text-muted'>No hay datos para calcular</p>"})
        
        resultados = []
        total_general = 0
        
        for modulo, forms in quote_data.items():
            for form in forms:
                try:
                    # --- Validación de datos del formulario ---
                    largo = float(form.get("largo") or 0)
                    ancho = float(form.get("ancho") or 0)
                    panel_id = int(form.get("tipoPanel") or 0)

                    if not (largo > 0 and ancho > 0 and panel_id):
                        print(f"⚠️ Formulario incompleto para {modulo}: {form}")
                        continue

                    # --- Obtener panel y su información ---
                    panel = PanelSIP.objects.get(id=panel_id)

                    # Buscar imagen asociada (si existe)
                    imagen_rel = panel.imagenes.first()
                    imagen_url = imagen_rel.imagen.url if imagen_rel else "/static/img/SinImagen.png"

                    # --- Calcular áreas ---
                    area_total = largo * ancho  # en m² (viene del formulario)
                    area_panel = (float(panel.largo) * float(panel.ancho)) / 10000  # cm² → m²

                    if area_panel <= 0:
                        area_panel = 2.88  # valor por defecto si los datos del panel no son válidos

                    # --- Cálculos de cantidad y precios ---
                    cantidad = max(1, round(area_total / area_panel))  # paneles enteros
                    total = cantidad * float(panel.precio_actual)
                    total_general += total

                    resultados.append({
                        "nombre": panel.nombre,
                        "imagen": imagen_url,
                        "solicitado_por": modulo,
                        "area": round(area_total, 2),
                        "cantidad": cantidad,
                        "valor": round(panel.precio_actual, 2),
                        "total": round(total, 2),
                    })

                except PanelSIP.DoesNotExist:
                    print(f"⚠️ Panel con ID {form.get('tipoPanel')} no existe.")
                except Exception as e:
                    print(f"⚠️ Error calculando {modulo}: {e}")

        # --- Renderizar tabla parcial ---
        html = render(request, "partials/calculo_resultado.html", {
            "resultados": resultados,
            "total_general": total_general
        }).content.decode("utf-8")

        return JsonResponse({"html": html})

@csrf_exempt
def limpiar_calculo(request):
    request.session["quote_forms"] = {}
    request.session.modified = True
    return JsonResponse({"message": "Cálculo limpiado"})