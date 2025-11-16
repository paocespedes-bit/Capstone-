from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from store.models import PanelSIP, KitConstruccion
from control.models import Local, Pedido, DetallePedido 
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST
from .carrito import Carrito
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import mercadopago


def carrito(request):
    carrito = Carrito(request)
    productos_completos = carrito.obtener_productos_completos()
    locales = Local.objects.all()
    contiene_kit_bool = contiene_kit(carrito)
    
    context = {
        "public_key": settings.MERCADOPAGO_PUBLIC_KEY,
        'productos_carrito': productos_completos,
        'locales': locales,   
        'contiene_kit':contiene_kit_bool,
        }
    return render(request, "carrito.html", context)

def contiene_kit(carrito):
    try:
        kit_ct = ContentType.objects.get_for_model(KitConstruccion)
        kit_ct_id = str(kit_ct.id)

        for item in carrito.carrito.values():
            if str(item["content_type_id"]) == kit_ct_id:
                return True
            
            if item.get("is_from_quote", False):
                return True

        return False

    except Exception as e:
        print("Error detectando restricción de pago (Kit o Cotización):", e)
        return False


def obtener_producto_concreto(producto_id, content_type_id):
    try:
        content_type = ContentType.objects.get_for_id(content_type_id)
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


@require_POST
def agregar_producto(request):
    try:
        data = json.loads(request.body)
        producto_id = data.get('id')
        content_type_id = data.get('ctid')
        cantidad = int(data.get('cantidad', 1))
        is_from_quote = data.get('is_from_quote', False)

        producto = obtener_producto_concreto(producto_id, content_type_id)
        if not producto:
            return JsonResponse({"error": "Producto no encontrado."}, status=404)

        producto_dict = {
            'id': producto.id,
            'nombre': producto.nombre,
            'precio_actual': producto.precio_actual,
            'content_type_id': content_type_id,
            'is_from_quote': is_from_quote,
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
    


# ==============================================
# 🛒 CREAR PEDIDO TEMPORAL
# ==============================================
PENDING_ORDERS = {}

@require_POST
def crear_pedido(request):
    """Crea un pedido temporal o completo según el método de pago."""
    carrito = Carrito(request)

    if not carrito.carrito:
        return JsonResponse({"error": "Tu carrito está vacío."}, status=400)

    try:
        local_id = request.POST.get('localSelect')
        metodo_pago = request.POST.get('paymentMethod')
        comprador = request.POST.get('clientName')
        rut_cli = request.POST.get('clientRut')
        correo_cli = request.POST.get('clientEmail')
        celular_cli = request.POST.get('clientPhone')
        ubicacion_cli = request.POST.get('clientAddress')

        local = Local.objects.get(id=local_id) if local_id else None

        # 🟩 Pago en tienda: crea pedido completo (CORRECCIÓN AQUÍ)
        if metodo_pago == 'store':
            # --- (El resto de la creación del Pedido y DetallePedido es correcto) ---
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
                metodo_pago='pago_tienda',
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
            # ------------------------------------------------------------------------
            
            # 👇 CORRECCIÓN: Usar reverse() para la URL base y construir el parámetro GET
            redirect_url = f"{reverse('pago_exitoso')}?pedido_id={pedido.id}"

            return JsonResponse({
                "ok": True,
                "pedido_id": pedido.id,
                "redirect": redirect_url  # Redirección con pedido_id por GET
            })

        # 🟦 Pago online: guardar pedido temporal (para Mercado Pago) (El resto de la función es correcto)
        temp_id = str(timezone.now().timestamp())

        # 🧩 Agregamos el precio actual en cada ítem
        items_temp = []
        for item in carrito.carrito.values():
            try:
                precio = float(item.get('precio_actual') or item.get('precio') or item.get('precio_unitario') or 0)
            except (ValueError, TypeError):
                precio = 0

            items_temp.append({
                "producto_id": item.get("producto_id"),
                "nombre": item.get("nombre"),
                "cantidad": item.get("cantidad"),
                "precio_actual": precio,
                "content_type_id": item.get("content_type_id"),
            })

        # 🧠 Guardamos la info temporalmente
        PENDING_ORDERS[temp_id] = {
            "local_id": local_id,
            "comprador": comprador,
            "rut_cli": rut_cli,
            "correo_cli": correo_cli,
            "celular_cli": celular_cli,
            "ubicacion_cli": ubicacion_cli,
            "items": items_temp
        }

        carrito.limpiar()

        return JsonResponse({"ok": True, "temp_id": temp_id})

    except Exception as e:
        print("❌ ERROR crear_pedido:", str(e))
        return JsonResponse({"error": f"Error al crear pedido temporal: {str(e)}"}, status=500)


# ==============================================
# 💳 CREAR PREFERENCIA MERCADO PAGO
# ==============================================
@csrf_exempt
def crear_preferencia(request):
    try:
        data = json.loads(request.body)
        temp_id = data.get("temp_id")

        if not temp_id:
            return JsonResponse({"error": "No se recibió temp_id"}, status=400)

        pedido_temp = PENDING_ORDERS.get(temp_id)
        if not pedido_temp:
            return JsonResponse({"error": "No se encontró información temporal del pedido."}, status=404)

        MERCADOPAGO_ACCESS_TOKEN = settings.MERCADOPAGO_ACCESS_TOKEN
        sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)

        # 🔹 Construcción de items
        items = []
        for item in pedido_temp["items"]:
            items.append({
                "title": item["nombre"],
                "quantity": int(item["cantidad"]),
                "currency_id": "CLP",
                "unit_price": float(item["precio_actual"]),
            })

        # ✅ URLs válidas
        host = request.get_host()
        scheme = 'https'

        success_url = f"{scheme}://{host}/procesando_pago/?temp_id={temp_id}"
        failure_url = f"{scheme}://{host}/pago_fallido/"
        pending_url = f"{scheme}://{host}/procesando_pago/?temp_id={temp_id}"

        preference_data = {
            "items": items,
            "back_urls": {
                "success": success_url,
                "failure": failure_url,
                "pending": pending_url,
            },
            "auto_return": "approved",
            "payer": {"email": pedido_temp.get("correo_cli", "cliente@example.com")},
            "external_reference": temp_id,
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response.get("response", {})

        if "id" not in preference:
            return JsonResponse({
                "error": "No se recibió ID de preferencia desde Mercado Pago",
                "response": preference_response,
            }, status=400)

        return JsonResponse(preference)

    except Exception as e:
        print("❌ ERROR crear_preferencia:", str(e))
        return JsonResponse({"error": str(e)}, status=500)



def procesando_pago(request):
    temp_id = request.GET.get("temp_id")
    if not temp_id or temp_id not in PENDING_ORDERS:
        messages.error(request, "No se encontró el pedido temporal.")
        return redirect("pago_fallido")

    data = PENDING_ORDERS.pop(temp_id)

    local = Local.objects.get(id=data["local_id"]) if data["local_id"] else None

    pedido = Pedido.objects.create(
        local=local,
        nombre_local=local.nombre if local else None,
        comprador=data["comprador"],
        rut_cli=data["rut_cli"],
        correo_cli=data["correo_cli"],
        celular_cli=data["celular_cli"],
        ubicacion_cli=data["ubicacion_cli"],
        fecha_pedido=timezone.now(),
        estado='pagado',
        metodo_pago='pago_web',
        monto_total=0
    )

    total = 0
    for item in data["items"]:
        content_type = ContentType.objects.get_for_id(item['content_type_id'])
        producto_obj = content_type.get_object_for_this_type(id=item['producto_id'])
        detalle = DetallePedido.objects.create(
            pedido=pedido,
            content_type=content_type,
            object_id=producto_obj.id,
            cantidad=item['cantidad']
        )
        total += detalle.subtotal

    pedido.monto_total = total
    pedido.save()

    return render(request, "procesando_pago.html", {"pedido_id": pedido.id})



def pago_exitoso(request):
    pedido_id = request.GET.get("pedido_id")
    pedido = None
    productos = []

    if pedido_id and pedido_id.isdigit():
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            detalles = DetallePedido.objects.filter(pedido=pedido)

            for d in detalles:
                content_type = d.content_type
                producto_obj = content_type.get_object_for_this_type(id=d.object_id)

                productos.append({
                    "nombre": getattr(producto_obj, "nombre", str(producto_obj)),
                    "cantidad": d.cantidad,
                    "subtotal": d.subtotal,
                })

        except Pedido.DoesNotExist:
            pedido = None

    context = {
        "pedido": pedido,
        "productos": productos,
    }

    return render(request, "pago_exitoso.html", context)



def pago_pendiente(request):
    pedido_id = request.GET.get("pedido_id")
    pedido = None
    if pedido_id and pedido_id.isdigit():
        try:
            pedido = Pedido.objects.get(id=pedido_id)
        except Pedido.DoesNotExist:
            pedido = None
    return render(request, "pago_pendiente.html", {"pedido": pedido})


def pago_fallido(request):
    return render(request, "pago_fallido.html")


