from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.filter
def decimal_point(value):
    if value is None:
        return "0.00"
    return str(value).replace(',', '.')

@register.filter
def punto_miles(value):
    try:
        value = int(value)
        return f"{value:,}".replace(",", ".")
    except (ValueError, TypeError):
        return value
    
@register.filter
def content_type(obj):
    return ContentType.objects.get_for_model(obj).id

@register.filter
def total_precio(carrito):
    if not carrito:
        return 0
    total = sum(item.get("acumulado", 0) for item in carrito.values())
    return total