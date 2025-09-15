from django.db import models

# !Crear los modelos aqui
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    precio =models.FloatField()
    espesor = models.FloatField(blank=True, null=True)
    ancho =  models.FloatField(blank=True, null=True)
    largo =  models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Imagen(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="imagenes")
    url_imagen = models.URLField(max_length=500)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return f"{self.producto.nombre}"

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE,related_name="inventario")
    disponible = models.IntegerField(default=0)
    reserva = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.producto.nombre}"

# class Comentario()

