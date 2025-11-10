from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from django import forms

# Obtener el modelo de usuario personalizado que definiste (CustomUser)
User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    # El campo 'username' es redefinido para aceptar correo o nombre de usuario.
    username = forms.CharField(
        label=_("Correo Electrónico o Nombre de Usuario"),
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
    )

    def clean(self):
        # Mantiene la validación estándar de password
        super().clean() 
        
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # 1. Intentar autenticar por username
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )

            # 2. Si falla, intentar autenticar por email
            if self.user_cache is None:
                try:
                    # Busca el usuario por email
                    user = User.objects.get(email__iexact=username)
                except User.DoesNotExist:
                    # Si no se encuentra por email, el error original es suficiente
                    pass
                else:
                    # Si lo encuentra, intenta autenticar con el username real
                    self.user_cache = authenticate(
                        self.request,
                        username=user.get_username(), # Usar el username real
                        password=password,
                    )
            
            # 3. Si ambos fallan, levanta el error de credenciales
            if self.user_cache is None:
                raise self.get_invalid_login_error()

        return self.cleaned_data