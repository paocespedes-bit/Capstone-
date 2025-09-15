from django.db import models

# !Crear los modelos aqui

# * Categorias
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nombre
    
# * Stock / Inventario
class Stock(models.Model):
    cantidad  = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.cantidad}"
    
# * Productos (Madre)
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.FloatField()
    # oferta =
    # stock =
    descripcion = models.TextField(blank=True, null=True)

    class Meta: 
        abstract = True 
    
    def __str__(self):
        return self.nombre
    
# * Kits de autoconstruccion
class KitConstruccion(Producto):
    m2 = models.DecimalField(max_digits=8, decimal_places=2)
    dormitorios = models.PositiveIntegerField(default=0)
    banos = models.PositiveIntegerField(default=0)
    categorias =models.ManyToManyField(Categoria, related_name="kits")

# * Paneles SiP
class PaneleSIP(Producto):
    tipo_obs = models.CharField(max_length=100, blank=True,null=True)
    madera_union = models.CharField(max_length=100, blank=True,null=True)
    espesor = models.DecimalField(max_digits=5, decimal_places=2)  # ! cm o mm?
    largo = models.DecimalField(max_digits=7, decimal_places=2)  
    ancho = models.DecimalField(max_digits=5, decimal_places=2)
    categorias =models.ManyToManyField(Categoria, related_name="paneles")  

# * Imagen 

def ruta_imagen(instance, filename):
    if instance.kit: # !si la imagen es de un kit 
        return f"kit/{filename}"
    elif instance.panel: # !si la imagen es de un panel
        return f"panel/{filename}"
    else: #! fallback por si no pertenece a ninguno
        return f"otros{filename}"

class imagenProducto(models.Model):
    kit = models.ForeignKey(KitConstruccion, related_name="imagenes", on_delete=models.CASCADE,null=True,blank=True)
    panel =models.ForeignKey(PaneleSIP,related_name="imagenes", on_delete=models.CASCADE, null=True,blank=True)
    imagen = models.ImageField(upload_to=ruta_imagen) #Guardar la imagen en carpeta correspondiente

    def __str__(self):
        return f"Imagen de {self.kit or self.panel}"






# _______________________________________________________________-



# class Inventario(models.Model):
#     producto = models.ForeignKey(Producto, on_delete=models.CASCADE,related_name="inventario")
#     disponible = models.IntegerField(default=0)
#     reserva = models.IntegerField(default=0)

#     def __str__(self):
#         return f"{self.producto.nombre}"

# # class Comentario()

