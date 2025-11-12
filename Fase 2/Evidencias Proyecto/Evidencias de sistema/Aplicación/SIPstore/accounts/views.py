from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import IdentifierForm, MethodForm, CodeForm, ResetForm
from .utils_verif import (
    create_code_session, get_data, clear_session, mark_used,
    increment_attempts, is_expired, remaining_seconds
)
from .utils_send import send_email_sendgrid, send_sms_mock
from .utils_mask import mask_email, mask_phone  
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse

User = get_user_model()

def forgot(request):
    if request.method == "POST":
        if request.POST.get("user_id"):
            form = MethodForm(request.POST)
            if form.is_valid():
                user_id = form.cleaned_data["user_id"]
                method = form.cleaned_data["method"]
                use_backup = form.cleaned_data["use_backup"]
                user = User.objects.filter(id=user_id).first()
                if not user:
                    messages.error(request, "Usuario no encontrado.")
                    return redirect("forgot")
                if method == "email":
                    dest = user.correo_de_respaldo if use_backup and user.correo_de_respaldo else user.email
                    if not dest:
                        messages.error(request, "No hay correo disponible para este usuario.")
                        return redirect("forgot")
                else:
                    dest = user.celular
                    if not dest:
                        messages.error(request, "No hay número de celular para este usuario.")
                        return redirect("forgot")
                code = create_code_session(request, user.id, method)
                sent = False
                if method == "email":
                    sent = send_email_sendgrid(dest, code)
                else:
                    sent = send_sms_mock(dest, code)
                if not sent:
                    messages.error(request, "Error al enviar el código. Intenta más tarde.")
                    clear_session(request)
                    return redirect("forgot")
                return redirect("verify")
        else:
            form = IdentifierForm(request.POST)
            if form.is_valid():
                ident = form.cleaned_data["identifier"].strip()
                user = User.objects.filter(email__iexact=ident).first() or User.objects.filter(username__iexact=ident).first()
                if not user:
                    messages.info(request, "Si la cuenta existe, se mostrará la opción para enviar un código.")
                    return render(request, "forgot.html", {"form": form, "user_obj": None})
                method_form = MethodForm(initial={"user_id": user.id})
                email_main = user.email
                email_backup = user.correo_de_respaldo
                phone = user.celular
                return render(request, "forgot.html", {
                    "form": form,
                    "user_obj": user,
                    "method_form": method_form,
                    "email_mask": mask_email(email_main) if email_main else None,
                    "email_backup_mask": mask_email(email_backup) if email_backup else None,
                    "phone_mask": mask_phone(phone) if phone else None,
                })
    else:
        form = IdentifierForm()
    return render(request, "forgot.html", {"form": form, "user_obj": None})

def verify(request):
    data = get_data(request)
    if not data:
        messages.error(request, "No hay proceso de recuperación activo.")
        return redirect("forgot")
    user = User.objects.filter(id=data["user_id"]).first()
    if not user:
        clear_session(request)
        messages.error(request, "Usuario inválido.")
        return redirect("forgot")

    dest_masked = mask_email(user.email) if data["method"] == "email" else mask_phone(user.celular)
    rem = remaining_seconds(data)

    if request.method == "POST":
        form = CodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"].strip()
            data = get_data(request)
            if not data:
                messages.error(request, "No hay datos en sesión.")
                return redirect("forgot")
            if is_expired(data):
                messages.error(request, "El código expiró. Puedes reenviarlo.")
                return redirect("forgot")
            if data.get("used"):
                messages.error(request, "El código ya fue usado.")
                return redirect("forgot")
            if code != data.get("code"):
                increment_attempts(request)
                messages.error(request, "Código incorrecto.")
                return redirect("verify")
            mark_used(request)
            return redirect("reset")
    else:
        form = CodeForm()
    return render(request, "verify.html", {"form": form, "dest_masked": dest_masked, "remaining": rem})

def resend(request):
    data = get_data(request)
    if not data:
        messages.error(request, "No hay proceso activo.")
        return redirect("forgot")
    if not is_expired(data):
        messages.info(request, "Aún tienes un código válido. Espera a que expire para reenviar.")
        return redirect("verify")
    user = User.objects.filter(id=data["user_id"]).first()
    if not user:
        clear_session(request)
        messages.error(request, "Usuario inválido.")
        return redirect("forgot")
    method = data["method"]
    code = create_code_session(request, user.id, method)
    if method == "email":
        sent = send_email_sendgrid(user.email, code)
    else:
        sent = send_sms_mock(user.celular, code)
    if not sent:
        messages.error(request, "Error al reenviar código.")
        clear_session(request)
        return redirect("forgot")
    messages.success(request, "Código reenviado.")
    return redirect("verify")

def reset(request):
    data = get_data(request)
    if not data or not data.get("used"):
        messages.error(request, "Debes validar el código primero.")
        return redirect("forgot")
    user = User.objects.filter(id=data["user_id"]).first()
    if not user:
        clear_session(request)
        messages.error(request, "Usuario inválido.")
        return redirect("forgot")

    if request.method == "POST":
        form = ResetForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["password1"])
            user.save()
            clear_session(request)
            return redirect("done")
    else:
        form = ResetForm()
    return render(request, "reset.html", {"form": form})

def done(request):
    return render(request, "done.html")


def profile(request):
    return render(request, "profile.html")

@login_required
def update(request):
    """Maneja la actualización de campos de usuario y la contraseña."""
    if request.method == 'POST':
        # 1. ACTUALIZACIÓN DE DATOS NORMALES (Modal: editUserModal)
        if 'field_to_update' in request.POST and 'new_value' in request.POST:
            field = request.POST.get('field_to_update')
            new_value = request.POST.get('new_value')
            
            # Lista de campos permitidos para evitar inyecciones maliciosas
            allowed_fields = ['username', 'email', 'correo_de_respaldo', 'celular']
            
            if field in allowed_fields:
                try:
                    # Validaciones básicas de no vacíos
                    if not new_value:
                        messages.error(request, f"El campo {field.replace('_', ' ').title()} no puede estar vacío.")
                        return redirect('profile') 
                    
                    # Validación específica para Email
                    if field == 'email' and not '@' in new_value:
                        messages.error(request, "El correo electrónico no es válido.")
                        return redirect('profile')
                    
                    # Actualizar el valor en el objeto de usuario
                    setattr(request.user, field, new_value)
                    request.user.full_clean() # Ejecuta validaciones del modelo (ej: unique=True)
                    request.user.save()
                    
                    messages.success(request, f"{field.replace('_', ' ').title()} actualizado exitosamente.")
                    return redirect('profile') 

                except Exception as e:
                    # Captura errores de validación del modelo (ej: username ya existe)
                    messages.error(request, f"Error al actualizar {field.replace('_', ' ').title()}: {e}")
                    return redirect('profile')

        # 2. ACTUALIZACIÓN DE CONTRASEÑA (Modal: editPassModal)
        elif 'new_password' in request.POST and 'confirm_password' in request.POST:
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password and new_password == confirm_password:
                # Usar la función set_password de Django
                request.user.set_password(new_password)
                request.user.save()
                
                # Importante: Mantener la sesión del usuario después de cambiar la contraseña
                update_session_auth_hash(request, request.user) 
                
                messages.success(request, 'Contraseña actualizada exitosamente. Su sesión se ha mantenido.')
                return redirect('profile') 
            
            elif new_password != confirm_password:
                messages.error(request, 'Las contraseñas no coinciden.')
                return redirect('profile')
            
            else:
                messages.error(request, 'Ambos campos de contraseña son requeridos.')
                return redirect('profile')
                
    return redirect('profile')