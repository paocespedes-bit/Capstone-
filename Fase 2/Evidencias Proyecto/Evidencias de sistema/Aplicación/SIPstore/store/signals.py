from django.core.mail import send_mail
from django.conf import settings

def enviar_alerta_stock_bajo(nombre_producto, cantidad, email_admin=None):
    """
    Envía una alerta cuando el stock disponible baja de 10 unidades.
    """
    subject = f"⚠️ Stock bajo: {nombre_producto}"
    message = f"El producto '{nombre_producto}' tiene solo {cantidad} unidades disponibles."

    destinatario = email_admin or getattr(settings, "DEFAULT_FROM_EMAIL", None)

    if destinatario:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [destinatario],
            fail_silently=False,
        )
    else:
        # En modo desarrollo, solo mostramos el mensaje
        print(f"[ALERTA STOCK BAJO] {subject} - {message}")

def enviar_alerta_stock_multiple(productos_alerta, email_admin=None):
    """
    Envía un solo correo con todos los productos con bajo stock.
    productos_alerta = [{'nombre': 'Panel OSB', 'disponible': 8}, ...]
    """
    if not productos_alerta:
        return

    subject = "⚠️ Alerta: varios productos con stock bajo"
    body_lines = [
        "Se detectaron productos con menos de 10 unidades disponibles:\n"
    ]

    for p in productos_alerta:
        body_lines.append(f"• {p['nombre']}: {p['disponible']} unidades disponibles")

    message = "\n".join(body_lines)

    destinatario = email_admin or getattr(settings, "DEFAULT_FROM_EMAIL", None)

    if destinatario:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [destinatario])
    else:
        print(f"[ALERTA STOCK MÚLTIPLE]\n{message}")