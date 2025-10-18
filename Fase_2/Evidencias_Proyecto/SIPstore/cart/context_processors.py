def totales_carrito(request):
    # Obtiene el carrito de la sesión. Si no existe o no es un diccionario, usa un diccionario vacío {}.
    carrito = request.session.get("carrito", {})
    if not isinstance(carrito, dict):
        carrito = {}
        
    total = 0
    cantidad_articulos = 0
    
    # Ahora puedes llamar .items() de forma segura, ya que 'carrito' es garantizado un diccionario.
    for key, value in carrito.items():
        # Asume que 'value' es un diccionario que contiene 'precio' y 'cantidad'
        try:
            total += int(value["precio"]) * value["cantidad"]
            cantidad_articulos += value["cantidad"]
        except (TypeError, ValueError, KeyError):
            # Manejo de errores si los datos dentro del carrito no son correctos
            continue 

    return {
        "total_carrito": total,
        "cantidad_articulos_carrito": cantidad_articulos
    }