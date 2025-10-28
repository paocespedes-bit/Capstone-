from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from store.models import PanelSIP, KitConstruccion
from control.models import Local, Pedido, DetallePedido 
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST
from .carrito import Carrito
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse, NoReverseMatch
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import mercadopago


def carrito(request):
    carrito = Carrito(request)
    productos_completos = carrito.obtener_productos_completos()
    locales = Local.objects.all()
    
    context = {
        "public_key": settings.MERCADOPAGO_PUBLIC_KEY,
        'productos_carrito': productos_completos,
        'locales': locales,
    }
    return render(request, "carrito.html", context)


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


@csrf_exempt
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

@csrf_exempt
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
    

# !Pedidos 
def crear_pedido(request):
    if request.method == 'POST':
        carrito = Carrito(request)

        if not carrito.carrito:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"error": "Tu carrito está vacío."}, status=400)
            messages.error(request, "Tu carrito esta vacio")
            return redirect('carrito')

        try:
            local_id = request.POST.get('localSelect')
            metodo_pago = request.POST.get('paymentMethod')
            comprador = request.POST.get('clientName')
            rut_cli = request.POST.get('clientRut')
            correo_cli = request.POST.get('clientEmail')
            celular_cli = request.POST.get('clientPhone')
            ubicacion_cli = request.POST.get('clientAddress')

            local = Local.objects.get(id=local_id) if local_id else None

            pedido = Pedido.objects.create(
                local=local,
                nombre_local=local.nombre if local else None,
                comprador=comprador,
                rut_cli=rut_cli,
                correo_cli=correo_cli,
                celular_cli=celular_cli,
                ubicacion_cli=ubicacion_cli,
                fecha_pedido=timezone.now(),
                estado='pendiente',
                metodo_pago='pago_web' if metodo_pago == 'online' else 'pago_tienda',
                monto_total=0
            )

            monto_total = 0

            for item in carrito.carrito.values():
                content_type = ContentType.objects.get_for_id(item['content_type_id'])
                producto_obj = content_type.get_object_for_this_type(id=item['producto_id'])
                cantidad = item['cantidad']

                detalle = DetallePedido.objects.create(
                    pedido=pedido,
                    content_type=content_type,
                    object_id=producto_obj.id,
                    cantidad=cantidad
                )
                monto_total += detalle.subtotal

            pedido.monto_total = monto_total
            pedido.save()
            carrito.limpiar()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"ok": True, "pedido_id": pedido.id})

            messages.success(request, f"Pedido #{pedido.id} creado exitosamente.")
            return redirect('pedido_exitoso')

        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"error": str(e)}, status=500)
            messages.error(request, "Ocurrió un error al crear el pedido. Intenta nuevamente.", e)
            return redirect('carrito')

    return redirect('ver_carrito')



# !Mercado PAGO:
@csrf_exempt
def crear_preferencia(request):
    carrito = Carrito(request)
    if not carrito.carrito:
            messages.error(request, "Tu carrito esta vacio")
            return redirect('carrito')
    try:
        MERCADOPAGO_ACCESS_TOKEN = settings.MERCADOPAGO_ACCESS_TOKEN 
        sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)
        items = []
        total = 0
        
        host = request.get_host()
        scheme = 'https'
        
        success_path = reverse('pago_exitoso')
        failure_path = reverse('pago_fallido')
        pending_path = reverse('pago_pendiente')
        
        success_url = f"{scheme}://{host}{success_path}"
        failure_url = f"{scheme}://{host}{failure_path}"
        pending_url = f"{scheme}://{host}{pending_path}"

        print(f"DEBUG MP Success URL: {success_url}")
        
        for item in carrito.carrito.values():
            items.append({
                "title": item["nombre"],
                "quantity": int(item["cantidad"]),
                "currency_id": "CLP",
                "unit_price": float(item["precio_unitario"]),
                
            })
            total += float(item["acumulado"])
        
        payer_data = {
        # Es crucial para pasar las validaciones del formulario de pago (422)
        "email": "" 
        }
            
        preference_data = {
            "items": items,
            "back_urls": {
            "success": success_url,
            "failure": failure_url,
            "pending": pending_url
            },
            "auto_return": "approved",
            "payer_data":payer_data,
        }
        
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        
        print(preference_response)  # <--- depuración
        preference = preference_response.get("response")
        print(preference)
        return JsonResponse(preference)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    


def pago_exitoso(request):
    return render(request, "pago_exitoso.html")

def pago_fallido(request):
    return render(request, "pago_fallido.html")

def pago_pendiente(request):
    return render(request, "pago_pendiente.html")