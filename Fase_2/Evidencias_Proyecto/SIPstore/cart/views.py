from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .carrito import Carrito
from django.views.decorators.http import require_POST

def carrito(request):
    return render(request, "carrito.html", {})


# Función para obtener producto por content_type + id
def get_producto(content_type_id, producto_id):
    try:
        content_type = ContentType.objects.get(id=content_type_id)
        return content_type.get_object_for_this_type(id=producto_id)
    except (ContentType.DoesNotExist, ValueError):
        return None

# Agregar producto al carrito
def agregar_producto(request):
    if request.method == "POST":
        producto_id = request.POST.get("producto_id")
        content_type_id = request.POST.get("content_type")
        cantidad = int(request.POST.get("cantidad", 1))

        producto = get_producto(content_type_id, producto_id)
        if not producto:
            return JsonResponse({"ok": False, "msg": "Producto no encontrado."}, status=404)

        carrito = Carrito(request)
        carrito.agregar(producto, cantidad)

        return JsonResponse({
            "ok": True,
            "msg": f"✅ {producto.nombre} agregado al carrito.",
            "total": carrito.total_precio(),
            "cantidad_total": carrito.total_productos(),
        })

# Restar unidades de un producto
def restar_producto(request):
    if request.method == "POST":
        producto_id = request.POST.get("producto_id")
        content_type_id = request.POST.get("content_type")
        cantidad = int(request.POST.get("cantidad", 1))

        producto = get_producto(content_type_id, producto_id)
        if not producto:
            return JsonResponse({"ok": False, "msg": "Producto no encontrado."}, status=404)

        carrito = Carrito(request)
        carrito.restar(producto, cantidad)

        return JsonResponse({
            "ok": True,
            "msg": f"➖ Se restó {cantidad} unidad(es) de {producto.nombre}.",
            "total": carrito.total_precio(),
            "cantidad_total": carrito.total_productos(),
        })

# Eliminar producto del carrito
def eliminar_producto(request):
    if request.method == "POST":
        producto_id = request.POST.get("producto_id")
        content_type_id = request.POST.get("content_type")

        producto = get_producto(content_type_id, producto_id)
        if not producto:
            return JsonResponse({"ok": False, "msg": "Producto no encontrado."}, status=404)

        carrito = Carrito(request)
        carrito.eliminar(producto)

        return JsonResponse({
            "ok": True,
            "msg": f"🗑️ {producto.nombre} eliminado del carrito.",
            "total": carrito.total_precio(),
            "cantidad_total": carrito.total_productos(),
        })

# Limpiar carrito completo
def limpiar_carrito(request):
    if request.method == "POST":
        carrito = Carrito(request)
        carrito.limpiar()
        return JsonResponse({
            "ok": True,
            "msg": "🧹 Carrito vaciado.",
            "total": 0,
            "cantidad_total": 0,
        })
    return JsonResponse({"ok": False, "msg": "Método no permitido"}, status=405)