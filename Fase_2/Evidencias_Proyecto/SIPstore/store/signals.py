
# store/signals.py
from control.models import DetallePedido
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Inventario
from django.core.mail import send_mail

@receiver(post_save, sender=Inventario)
def verificar_stock_bajo(sender, instance, **kwargs):
    # Usamos el campo disponible existente
    producto_obj = instance.producto  # debe ser el objeto real
    if producto_obj:  # verifica que exista
        if instance.disponible < 10:
            subject = f"⚠️ Stock bajo para {getattr(producto_obj, 'nombre', 'Producto Desconocido')}"
            message = f"El inventario del producto ha bajado a {instance.disponible} unidades."
            send_mail(
                subject,
                message,
                'paoloignaciocespedestolhuysen@gmail.com',  # Remitente
                ['paoloignaciocespedestolhuysen@gmail.com'], # Destinatario
                fail_silently=True,
            )