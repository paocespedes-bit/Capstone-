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

    for item in carrito:
        ct = item["content_type"]
        product_id = item["product_id"]
        quantity = item["quantity"]
        
        # # Obtener el objeto real según su tipo
        # if ct == "kitconstruccion":
        #     producto = KitConstruccion.objects.filter(id=product_id).first()
        # elif ct == "panelesip":
        #     producto = PanelSIP.objects.filter(id=product_id).first()
        # else:
        #     producto = None

        # if producto:
        #     productos.append({
        #         # "producto": producto,
        #         "quantity": quantity,
        #         "content_type": ct
        #     })

    context = {
        "productos": productos,
        "carrito": carrito
    }
    return render(request, "carrito.html",context)

def agregar_carrito(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content_type = data.get("content_type")
        product_id = data.get("product_id")
        quantity = int(data.get("quantity", 1))
        
        carrito = request.session.get("carrito",[])
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
        del request.session["carrito"]  # elimina la clave carrito
        request.session.modified = True  # asegura que Django guarde el cambio
    return redirect("carrito") 