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


    """
    Ofusca correos electrónicos o números de teléfono.
    - Correo: c*****6@*****.com
    - Teléfono: *****1951
    """
    if not value:
        return ""
    
    value = str(value).strip()

    if type == 'email':
        try:
            name, domain = value.split('@')
            
            # Ofuscar nombre de usuario: Muestra el primer carácter + asteriscos + el último
            if len(name) > 2:
                obfuscated_name = name[0] + ('*' * (len(name) - 2)) + name[-1]
            elif len(name) > 0:
                obfuscated_name = name[0] + ('*' * (len(name) - 1))
            else:
                obfuscated_name = '*****' # Caso de nombre de usuario muy corto
            
            # Ofuscar dominio: Mostrar solo el dominio de nivel superior, o simplificar
            # Simplemente reemplazar el dominio con asteriscos, manteniendo el TLD (ej: .com)
            domain_parts = domain.split('.')
            if len(domain_parts) > 1:
                tld = domain_parts[-1] # TLD (.com, .org, etc.)
                obfuscated_domain = ('*' * len('.'.join(domain_parts[:-1]))) + '.' + tld
            else:
                obfuscated_domain = '*****.***'

            return mark_safe(f"{obfuscated_name}@{obfuscated_domain}")
            
        except ValueError:
            # No es un correo electrónico válido
            return 'Correo Inválido'

    elif type == 'phone':
        # Ofuscar teléfono: Mostrar asteriscos + los últimos 4 dígitos
        phone_digits = ''.join(filter(str.isdigit, value))
        if len(phone_digits) >= 4:
            last_four = phone_digits[-4:]
            obfuscated_phone = ('*' * (len(phone_digits) - 4)) + last_four
            return mark_safe(obfuscated_phone)
        else:
            # Número muy corto
            return '***'

    return value