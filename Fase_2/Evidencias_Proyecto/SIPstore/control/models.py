from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from store.models import PanelSIP, KitConstruccion,Inventario
# Create your models here.

# ! Modelo Local (local retiro)
class Local(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    ubicacion = models.CharField(max_length=300)
    telefono = models.CharField(max_length=20,blank=True,null=True)
    def __str__(self):
        return self.nombre
    
# ! Modelo Pedido
class Pedido(models.Model):
    ESTADOS =[
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    METODO =[
        ('pago_tienda', 'Pago en Tienda'),
        ('pago_web', 'Pago Web'),
    ]
    
    local = models.ForeignKey('Local',on_delete=models.SET_NULL,null=True, blank=True,related_name='pedidos')
    nombre_local = models.CharField(max_length=200, blank=True, null=True)
    
    comprador = models.CharField(max_length=200)
    rut_cli = models.CharField(max_length=12)
    correo_cli = models.EmailField()
    celular_cli = models.CharField(max_length=20)
    ubicacion_cli = models.TextField(max_length=800)
    
    fecha_pedido = models.DateTimeField(default=timezone.now)
    fecha_retiro = models.DateTimeField(blank=True,null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS,default='pendiente')
    
    monto_total = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=20,choices=METODO ,default='pago_tienda')
    
    def save(self, *args, **kwargs):
        if self.local and not self.nombre_local:
            self.nombre_local = self.local.nombre
        super().save(*args, **kwargs)

    def actualizar_monto_total(self):
        total = sum(detalle.subtotal for detalle in self.detalles.all())
        Pedido.objects.filter(pk=self.pk).update(monto_total=total)

    def __str__(self):
        return f"Pedido #{self.id} - {self.comprador}"
    
# ! Modelo detalle Pedido
# ! Modelo detalle Pedido
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    producto = GenericForeignKey('content_type', 'object_id')
    nombre_producto = models.CharField(max_length=255)
    precio_unitario = models.DecimalField(max_digits=10,decimal_places=2)
    
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2,editable=False)
    def save(self, *args, **kwargs):
        self.subtotal = self.precio_unitario * self.cantidad
        super().save(*args, **kwargs)

    # Actualiza monto total
        self.pedido.actualizar_monto_total()

    # Actualiza inventario del producto si existe
        if self.content_type and self.object_id:
            inventario = Inventario.objects.filter(
            content_type=self.content_type,
            object_id=self.object_id
            ).first()
            if inventario:
                inventario.reservado += self.cantidad
                inventario.actualizar_stock()
    
    def __str__(self):
        return f"{self.nombre_producto} x {self.cantidad} (Pedido #{self.pedido.id})"