from store.models import PanelSIP, KitConstruccion
from django.contrib.contenttypes.models import ContentType

class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito
            
    def agregar(self, producto_dict, cantidad=1):
        id_str = str(producto_dict['id'])
        precio_unitario = float(producto_dict['precio_actual'])
        
        if  id_str not in self.carrito.keys():
            self.carrito[id_str] = {
                "producto_id": producto_dict['id'],
                "content_type_id": producto_dict['content_type_id'],
                "nombre": producto_dict['nombre'],
                "precio_unitario": precio_unitario,
                "cantidad": cantidad,
                "acumulado": precio_unitario * cantidad,
            }
        else:
            self.carrito[id_str]["cantidad"] += cantidad
            self.carrito[id_str]["acumulado"] += self.carrito[id_str]["precio_unitario"] * self.carrito[id_str]["cantidad"]
            
        self.guardar_carrito()
    
    def eliminar(self, producto_id):
        id_str = str(producto_id)
        
        if id_str in self.carrito:
            del self.carrito[id_str]
            self.guardar_carrito()
    
    def restar(self, producto_id, cantidad=1):
        id_str = str(producto_id)
        if id_str in self.carrito.keys():
            self.carrito[id_str]["cantidad"] -= cantidad
            
            if self.carrito[id_str]["cantidad"] <= 0:
                self.elimiar(producto_id)
            else:
                self.carrito[id_str]["acumulado"] = self.carrito[id_str]["precio_unitario"] * self.carrito[id_str]["cantidad"]
                
            self.guardar_carrito()
        
    def actualizar(self, producto_id, nueva_cantidad):
        id_str = str(producto_id)
        nueva_cantidad = int(nueva_cantidad)
        
        if id_str in self.carrito.keys():
            if nueva_cantidad <= 0:
                self.eliminar(producto_id)
            else:
                self.carrito[id_str]["cantidad"] = nueva_cantidad
                self.carrito[id_str]["acumulado"] = self.carrito[id_str]["precio_unitario"] * nueva_cantidad
                self.guardar_carrito()
    
    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True
    
    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
    
    def obtener_productos_completos(self):
        productos_completos = []
        for item in self.carrito.values():
            try:
                content_type = ContentType.objects.get_for_id(item['content_type_id'])
                producto_obj = content_type.get_object_for_this_type(id=item['producto_id'])
                
                imagen = producto_obj.imagenes.first().imagen.url if producto_obj.imagenes.exists() else None
                
                productos_completos.append({
                    'producto': producto_obj,
                    'cantidad': item['cantidad'],
                    'acumulado': item['acumulado'],
                    'precio_unitario': item['precio_unitario'],
                    'imagen': imagen
                })
                
            except Exception as e:
                print(f"Error al cargar producto {item['producto_id']}: {e}")
                
        return productos_completos    