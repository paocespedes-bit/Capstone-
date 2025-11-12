from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.forms import CustomAuthenticationForm 
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=CustomAuthenticationForm), name='login'),
    path('accounts/logged_out_confirm/', TemplateView.as_view(template_name='registration/logged_out_confirm.html'), name='logged_out_confirm'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('forgot/', views.forgot, name='forgot'),
    path('send-resend/', views.resend, name='resend'),
    path('verify/', views.verify, name='verify'),
    path('reset/', views.reset, name='reset'),
    path('done/', views.done, name='done'),
    path('profile/',views.profile, name="profile"),
    path('profile/actualizar/', views.update, name='update'),
]