from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email_sendgrid(to_email, code):

    subject = "Código de verificación"
    text = f"Tu código de verificación es: {code}\nEste código expira en pocos minutos."
    html = f"<p>Tu código de verificación es: <strong>{code}</strong></p><p>Si no solicitaste esto, ignora este correo.</p>"
    message = Mail(
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"),
        to_emails=to_email,
        subject=subject,
        plain_text_content=text,
        html_content=html,
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        resp = sg.send(message)
        return resp.status_code in (200, 202)
    except Exception as e:
        print("SendGrid error:", e)
        return False

def send_sms_mock(number, code):
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print(f"[MOCK SMS] Enviando código {code} a {number}")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    return True
