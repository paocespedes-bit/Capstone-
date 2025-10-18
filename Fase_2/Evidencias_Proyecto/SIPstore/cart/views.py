from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from store.models import PanelSIP, KitConstruccion
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST
from .carrito import Carrito

def obtener_producto_concreto(producto_id, content_type_id):
    try:
        content_type = ContentType.objects.get_for_id(content_type_id)
        # Usamos content_type para obtener el modelo concreto y su objeto.
        ProductoModelo = content_type.model_class()
        return ProductoModelo.objects.get(id=producto_id)
    except ContentType.DoesNotExist:
        return None
    except Exception:
        return None
    
def generar_respuesta(carrito):
    total = sum(item["acumulado"] for item in carrito.carrito.values())
    cantidad_total = sum(item["cantidad"] for item in carrito.carrito.values())
    
    return {
        "total_carrito": total,
        "cantidad_total": cantidad_total,
        "carrito_data": carrito.carrito
    }

def carrito(request):
    carrito = Carrito(request)
    productos_completos = carrito.obtener_productos_completos()
    
    context = {
        'productos_carrito': productos_completos,
    }
    return render(request, "cart/carrito.html", context)

@require_POST
def agregar_producto(request):
    try:
        data = json.loads(request.body)
        producto_id = data.get('id')
        content_type_id = data.get('ctid')
        cantidad = int(data.get('cantidad', 1))

        producto = obtener_producto_concreto(producto_id, content_type_id)
        if not producto:
            return JsonResponse({"error": "Producto no encontrado."}, status=404)
        
        producto_dict = {
            'id': producto.id,
            'nombre': producto.nombre,
            'precio_actual': producto.precio_actual,
            'content_type_id': content_type_id,
        }
        
        carrito = Carrito(request)
        carrito.agregar(producto_dict, cantidad)
        
        response_data = generar_respuesta(carrito)
        response_data["mensaje"] = f"'{producto.nombre}' (x{cantidad}) agregado al carrito."
        
        return JsonResponse(response_data)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_POST
def modificar_carrito(request, accion):
    try:
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        
        carrito = Carrito(request)
        
        if accion == 'eliminar':
            carrito.eliminar(producto_id)
            mensaje = "Producto eliminado del carrito."
            
        elif accion == 'restar':
            carrito.restar(producto_id)
            mensaje = "Una unidad eliminada del producto."
            
        elif accion == 'actualizar':
            nueva_cantidad = data.get('cantidad')
            if nueva_cantidad is None or int(nueva_cantidad) < 0:
                return JsonResponse({"error": "Cantidad inválida."}, status=400)
            
            carrito.actualizar(producto_id, nueva_cantidad)
            mensaje = "Carrito actualizado."
            
        elif accion == 'limpiar':
            carrito.limpiar()
            mensaje = "Carrito vaciado."
        else:
            return JsonResponse({"error": "Acción no válida."}, status=400)
        
        response_data = generar_respuesta(carrito)
        response_data["mensaje"] = mensaje
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)