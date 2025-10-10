from django import template

register = template.Library()

@register.filter
def decimal_point(value):
    if value is None:
        return "0.00"
    return str(value).replace(',', '.')
