from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from django import forms

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