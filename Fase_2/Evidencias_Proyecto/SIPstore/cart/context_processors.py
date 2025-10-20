def totales_carrito(request):
    carrito = request.session.get("carrito", {})
    if not isinstance(carrito, dict):
        carrito = {}
        
    total = 0
    cantidad_articulos = 0
    
    productos_detalles = []
    
    for key, item in carrito.items():
        try:
            nombre = item.get("nombre", "Producto Desconocido")
            cantidad = item.get("cantidad", 0)
            acumulado = item.get("acumulado", 0)
            total += acumulado
            cantidad_articulos += cantidad
            
            productos_detalles.append({
                "nombre": nombre,
                "cantidad": cantidad,
                "acumulado": acumulado,
                "producto_id": key, 
            })
            
        except (TypeError, ValueError, KeyError) as e:
            print(f"Error procesando ítem en el carrito: {e}")
            continue 

    return {
        "total_carrito": int(total),
        "cantidad_articulos_carrito": cantidad_articulos,
        "productos_detalles": productos_detalles,
    }