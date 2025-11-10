from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.forms import CustomAuthenticationForm # <-- Importa tu form
from django.views.generic import TemplateView

urlpatterns = [
    # ... otras URLs
    
    # Sobreescribe la vista de login con tu formulario personalizado
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomAuthenticationForm # <-- Usa el formulario
    ), name='login'),
    
    path('accounts/logged_out_confirm/', 
         TemplateView.as_view(template_name='registration/logged_out_confirm.html'),
         name='logged_out_confirm'),
    
    path('accounts/', include('django.contrib.auth.urls')), # Deja esto para logout, etc.
]