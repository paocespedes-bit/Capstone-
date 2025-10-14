from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
import json
from store.models import PanelSIP, KitConstruccion 

# Create your views here.
def carrito(request):
    carrito = request.session.get("carrito", [])
    productos = []
    
    nuevo_carrito = []
    
    for item in carrito:
        content_type_model = item["content_type"]
        product_id = item["product_id"]
        cantidad = item["quantity"]

        try:
            content_type = ContentType.objects.get(model=content_type_model)
            producto = content_type.get_object_for_this_type(id=product_id)
            
            productos.append({
                "nombre":getattr(producto, "nombre","Sin nombre"),
                "precio":getattr(producto, "precio", 0),
                "precio_anterior":getattr(producto, "precio", 0), #!Cambiar una vez implementado descuento
                "cantidad": cantidad,
                "subtotal": getattr(producto, "precio", 0) * cantidad,
                "tipo": content_type_model,
                "id": product_id
            })
            nuevo_carrito.append(item)
        except content_type.model_class().DoesNotExist:
            productos.append({
                "nombre": "Producto inexistente",
                "precio": 0,
                "precio_anterior": 0,
                "cantidad": cantidad,
                "subtotal": 0,
                "tipo": content_type_model,
                "id": product_id
            })
            
    request.session["carrito"] = nuevo_carrito
    total = sum(p["subtotal"] for p in productos)
    context = {
        "carrito": carrito,
        "productos": productos,
        "total": total
        
    }
    return render(request, "carrito.html",context)

def agregar_carrito(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content_type = data.get("content_type")
        product_id = data.get("product_id")
        quantity = int(data.get("quantity", 1))
        
        carrito = request.session.get("carrito", [])
        for item in carrito:
            if item["content_type"] == content_type and item["product_id"] == product_id:
                item["quantity"] += quantity
                break
        else:
            carrito.append({
                "content_type": content_type,
                "product_id": product_id,
                "quantity": quantity
            })

        request.session["carrito"] = carrito
        total_items = sum(item["quantity"] for item in carrito)
        
        return JsonResponse({
            "message": "Producto añadido al carrito",
            "total_items": total_items
        })
    
    return JsonResponse({"error": "Método no permitido"}, status=405)

def vaciar_carrito(request):
    if "carrito" in request.session:
        del request.session["carrito"]  
        request.session.modified = True  
    return redirect("carrito") 

def eliminar_item_carrito(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content_type = data.get("content_type")
        product_id = data.get("product_id")

        if not content_type or not product_id:
            return JsonResponse({"error": "Datos inválidos"}, status=400)

        carrito = request.session.get("carrito", [])

        # Buscar el item y eliminarlo
        for item in carrito:
            if item["content_type"] == content_type and item["product_id"] == int(product_id):
                carrito.remove(item)
                break  

        
        request.session["carrito"] = carrito
        total_items = sum(item.get("quantity", 0) for item in carrito)
        
        return JsonResponse({
            "message": "Producto eliminado del carrito",
            "total_items": total_items
        })

    return JsonResponse({"error": "Método no permitido"}, status=405)