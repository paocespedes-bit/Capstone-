from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from django import forms
from django.db.models import Q


User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Correo Electrónico o Nombre de Usuario"),
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
    )

    def clean(self):
        super().clean() 
        
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )

            if self.user_cache is None:
                try:
                    user = User.objects.get(email__iexact=username)
                except User.DoesNotExist:
                    pass
                else:
                    self.user_cache = authenticate(
                        self.request,
                        username=user.get_username(), 
                        password=password,
                    )
            
            if self.user_cache is None:
                raise self.get_invalid_login_error()

        return self.cleaned_data
    

class IdentifierForm(forms.Form):
    identifier = forms.CharField(
        label=_("Correo o usuario"),
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'email o usuario', 'autofocus': True}),
        max_length=254
    )

class MethodForm(forms.Form):
    method = forms.ChoiceField(
        choices=(('email','Enviar por correo'), ('sms','Enviar por SMS')),
        widget=forms.RadioSelect,
        label=_("Elige método")
    )
    use_backup = forms.BooleanField(required=False, label=_("Usar correo de respaldo (si existe)"))
    user_id = forms.IntegerField(widget=forms.HiddenInput)

class CodeForm(forms.Form):
    code = forms.CharField(
        max_length=6, min_length=6,
        widget=forms.TextInput(attrs={'class':'form-control text-center','placeholder':'------','autocomplete':'off'}),
        label=_("Código")
    )

class ResetForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Nueva contraseña'}),
        label=_("Nueva contraseña")
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Repetir contraseña'}),
        label=_("Repetir contraseña")
    )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        if p1 and len(p1) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        return cleaned