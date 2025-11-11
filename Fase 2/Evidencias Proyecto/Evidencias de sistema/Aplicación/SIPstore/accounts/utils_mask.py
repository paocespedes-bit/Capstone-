def mask_email(email):
    if not email or '@' not in email:
        return email
    local, domain = email.split('@', 1)
    masked_local = (local[:2] + '*****') if len(local) > 2 else (local[0] + '*****')
    parts = domain.split('.')
    if len(parts) > 1:
        tld = parts[-1]
        masked_domain = '*****.' + tld
    else:
        masked_domain = '*****'
    return f"{masked_local}@{masked_domain}"

def mask_phone(phone):
    if not phone:
        return phone
    s = ''.join([c for c in phone if c.isdigit()])
    if len(s) <= 4:
        return '*' * len(s)
    return '*' * (len(s)-4) + s[-4:]
