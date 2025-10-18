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
    if obj is None:
        return None
    return ContentType.objects.get_for_model(obj).id

@register.filter
def truncate_chars(value, max_length):
    if len(value) > max_length:
        return value[:max_length] + '...'
    return value