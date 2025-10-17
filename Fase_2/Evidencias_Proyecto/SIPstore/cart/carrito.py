from django.contrib.contenttypes.models import ContentType

class Carrito:
    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
        self.carrito = self.session["carrito"]

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def agregar(self, producto, cantidad=1):
        content_type = ContentType.objects.get_for_model(producto)
        key = f"{content_type.id}-{producto.id}"

        if key not in self.carrito:
            self.carrito[key] = {
                "producto_id": producto.id,
                "tipo": content_type.model,
                "nombre": producto.nombre,
                "precio_unitario": float(producto.precio_actual),
                "cantidad": cantidad,
                "acumulado": float(producto.precio_actual) * cantidad,
            }
        else:
            self.carrito[key]["cantidad"] += cantidad
            self.carrito[key]["acumulado"] += float(producto.precio_actual) * cantidad

        self.guardar_carrito()

    def eliminar(self, producto):
        content_type = ContentType.objects.get_for_model(producto)
        key = f"{content_type.id}-{producto.id}"
        if key in self.carrito:
            del self.carrito[key]
            self.guardar_carrito()

    def restar(self, producto, cantidad=1):
        content_type = ContentType.objects.get_for_model(producto)
        key = f"{content_type.id}-{producto.id}"
        if key in self.carrito:
            self.carrito[key]["cantidad"] -= cantidad
            self.carrito[key]["acumulado"] -= float(producto.precio_actual) * cantidad
            if self.carrito[key]["cantidad"] <= 0:
                self.eliminar(producto)
            else:
                self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

    def total_productos(self):
        return sum(item["cantidad"] for item in self.carrito.values())

    def total_precio(self):
        return sum(item["acumulado"] for item in self.carrito.values())