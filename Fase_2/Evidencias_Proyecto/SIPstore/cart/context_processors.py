def totales_carrito(request):
    total = 0
    cantidad_total = 0
    if "carrito" in request.session.keys():
        for key, value in request.session["carrito"].items():
            total += value.get("acumulado", 0) 
            cantidad_total += value.get("cantidad", 0)
            
    return {"total_carrito": total, "cantidad_total": cantidad_total}