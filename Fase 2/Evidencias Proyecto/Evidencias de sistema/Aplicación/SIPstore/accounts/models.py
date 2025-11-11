from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

class CustomUser(AbstractUser):
    celular = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name='Celular'
    )
    
    correo_de_respaldo = models.EmailField(
        max_length=254, 
        unique=True, 
        blank=True, 
        null=True, 
        verbose_name='Correo de Respaldo'
    )

    TIPO_USUARIO_CHOICES = (
        ('CONTROL', 'Personal de Control'),
        ('ADMIN', 'Super Administrador'),
    )
    tipo_usuario = models.CharField(
        max_length=10, 
        choices=TIPO_USUARIO_CHOICES, 
        default='CONTROL'
    )

    class Meta:
        verbose_name = 'Usuario Personalizado'
        verbose_name_plural = 'Usuarios Personalizados'
        
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

