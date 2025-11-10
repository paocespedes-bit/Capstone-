# authentication/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Campos que ya existen en AbstractUser:
    # username, first_name, last_name (para nombre y apellido), email, password, is_superuser

    # Campos Adicionales:
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
    
    # Campo para el tipo de usuario (Si necesitas más de dos roles)
    # Si solo es 'Superusuario' o 'Control', puedes usar 'is_superuser' o 'is_staff'.
    TIPO_USUARIO_CHOICES = (
        ('CONTROL', 'Personal de Control'),
        ('ADMIN', 'Super Administrador'),
        # Puedes añadir más roles si es necesario
    )
    tipo_usuario = models.CharField(
        max_length=10, 
        choices=TIPO_USUARIO_CHOICES, 
        default='CONTROL'
    )

    # Puedes hacer que el campo 'email' sea el campo de identificación principal si lo deseas
    # En ese caso, debes definir: USERNAME_FIELD = 'email'
    # y eliminar 'email' de REQUIRED_FIELDS.

    class Meta:
        verbose_name = 'Usuario Personalizado'
        verbose_name_plural = 'Usuarios Personalizados'
        
    def get_full_name(self):
        """Retorna el nombre y apellido, que usarás como 'Nombre'"""
        return f"{self.first_name} {self.last_name}"