def totales_carrito(request):
    carrito = request.session.get("carrito", {})
    if not isinstance(carrito, dict):
        carrito = {}
        
    total = 0
    cantidad_articulos = 0
    
    for key, value in carrito.items():
        try:
            total += int(value["precio"]) * value["cantidad"]
            cantidad_articulos += value["cantidad"]
        except (TypeError, ValueError, KeyError):
            continue 

    return {
        "total_carrito": total,
        "cantidad_articulos_carrito": cantidad_articulos
    }