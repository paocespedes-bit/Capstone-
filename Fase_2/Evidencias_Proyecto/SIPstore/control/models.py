from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from store.models import PanelSIP, KitConstruccion,Inventario
from django.core.mail import send_mail
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._estado_original = self.estado  # Guardamos el estado inicial

    def save(self, *args, **kwargs):
        # Mantener el nombre del local
        if self.local and not self.nombre_local:
            self.nombre_local = self.local.nombre

        # Guardar el estado anterior antes de guardar
        estado_anterior = getattr(self, "_estado_original", None)

        # Guardar el pedido normalmente
        super().save(*args, **kwargs)

        # Si el estado cambió, actualizar el stock
        if estado_anterior != self.estado:
            self.actualizar_stock_por_estado()

        # Actualizar el estado original para futuras comparaciones
        self._estado_original = self.estado

    def actualizar_monto_total(self):
        total = sum(detalle.subtotal for detalle in self.detalles.all())
        Pedido.objects.filter(pk=self.pk).update(monto_total=total)
    
    def actualizar_stock_por_estado(self):
        """
        Ajusta el stock de los productos del pedido según el cambio de estado.
        Evita duplicar reservas al pasar entre 'pendiente' y 'en_proceso'.
        """
        # Si el estado no cambió, no hacemos nada
        if self.estado == getattr(self, "_estado_original", None):
            return
        
        for detalle in self.detalles.all():  # related_name='detalles' en DetallePedido
            if not detalle.content_type or not detalle.object_id:
                continue  # Saltar si no hay producto

            inventario = Inventario.objects.filter(
                content_type=detalle.content_type,
                object_id=detalle.object_id
            ).first()
            if not inventario:
                continue  # Si no existe inventario, ignorar

            estado_anterior = getattr(self, "_estado_original", None)
            estado_actual = self.estado

            # 🟢 Caso 1: Cambio a completado → liberar reserva (pedido entregado)
            if estado_anterior in ['pendiente', 'en_proceso'] and estado_actual == 'completado':
                nuevo_reservado = max(inventario.reservado - detalle.cantidad, 0)
                inventario.ajustar_reservado(nuevo_reservado)

            # 🔴 Caso 2: Cambio a cancelado → liberar reserva y devolver stock a disponible
            elif estado_anterior in ['pendiente', 'en_proceso'] and estado_actual == 'cancelado':
                nuevo_reservado = max(inventario.reservado - detalle.cantidad, 0)
                inventario.ajustar_reservado(nuevo_reservado)
                inventario.disponible += detalle.cantidad
                inventario.save(update_fields=['disponible', 'reservado'])

            # 🟡 Caso 3: Cambio desde cancelado/completado → pendiente o en_proceso → volver a reservar
            elif estado_anterior in ['completado', 'cancelado'] and estado_actual in ['pendiente', 'en_proceso']:
                inventario.ajustar_reservado(inventario.reservado + detalle.cantidad)

            # 🟣 Caso 4: Cambio de completado → cancelado (devolución)
            elif estado_anterior == 'completado' and estado_actual == 'cancelado':
                inventario.disponible += detalle.cantidad 
                inventario.save(update_fields=['disponible'])

            elif estado_anterior == 'cancelado' and estado_actual == 'completado':
                # Reducir el stock disponible porque el pedido ahora se completó
                if inventario.disponible >= detalle.cantidad:
                    inventario.disponible -= detalle.cantidad
                else:
                    # Manejo de excepción opcional: no hay suficiente stock
                    inventario.disponible = 0
                inventario.save(update_fields=['disponible'])

    def __str__(self):
        return f"Pedido #{self.id} - {self.comprador}"
            
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
        # Si existe un producto vinculado, copiamos su nombre y precio actual
        if self.producto:
            self.nombre_producto = getattr(self.producto, 'nombre', 'Producto Desconocido')
            self.precio_unitario = getattr(self.producto, 'precio_actual', 0)
        
        # Calculamos el subtotal antes de guardar
        self.subtotal = self.precio_unitario * self.cantidad
        
        super().save(*args, **kwargs)
        
        # Actualizamos el monto total del pedido
        self.pedido.actualizar_monto_total()

        # Actualizamos inventario: descontamos disponible y sumamos reservado
        if self.content_type and self.object_id:
            inventario = Inventario.objects.filter(
                content_type=self.content_type,
                object_id=self.object_id
            ).first()
            if inventario:
                # Restar disponible y sumar reservado
                inventario.disponible = max(inventario.disponible - self.cantidad, 0)
                inventario.reservado += self.cantidad
                inventario.save(update_fields=['disponible', 'reservado'])

