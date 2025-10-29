
# store/signals.py
from control.models import DetallePedido
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Inventario
from django.core.mail import send_mail

@receiver(post_save, sender=Inventario)
def verificar_stock_bajo(sender, instance, **kwargs):
    producto_obj = instance.producto
    if not producto_obj:
        # Intentar usar el nombre guardado en DetallePedido como fallback
        detalle = DetallePedido.objects.filter(
            content_type=instance.content_type,
            object_id=instance.object_id
        ).first()
        nombre_producto = detalle.nombre_producto if detalle else 'Producto Desconocido'
    else:
        nombre_producto = getattr(producto_obj, 'nombre', 'Producto Desconocido')
    if producto_obj and instance.disponible < 10:
        nombre_producto = getattr(producto_obj, 'nombre', 'Producto Desconocido')
        subject = f"⚠️ Stock bajo para {nombre_producto}"
        message = f"El inventario del producto ha bajado a {instance.disponible} unidades disponibles, con {instance.reservado} unidades reservadas."
        send_mail(
            subject,
            message,
            'paoloignaciocespedestolhuysen@gmail.com',  # Remitente
            ['paoloignaciocespedestolhuysen@gmail.com'], # Destinatario
            fail_silently=True,
        )