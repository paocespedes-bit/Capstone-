from .carrito import Carrito

def total_carrito(request):
    carrito = Carrito(request)
    return {"cantidad_total": carrito.total_productos()}