import sendgrid
from sendgrid.helpers.mail import Mail
from django.conf import settings
from python_http_client.exceptions import HTTPError
import os
from sendgrid import SendGridAPIClient


def enviar_correo_estado(correo_cli, asunto, mensaje_html):
    
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=correo_cli,
        subject=asunto,
        html_content=mensaje_html
    )

    try:
        response = sg.send(message)
        print(f"✅ Correo enviado a {correo_cli} (status {response.status_code})")
    except HTTPError as e:
        print(f"❌ Error al enviar correo a {correo_cli}: {e}")
        raise e
