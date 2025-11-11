from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'get_full_name', 'tipo_usuario', 'is_staff')
    
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'tipo_usuario', 'groups')
    
    search_fields = ('username', 'first_name', 'last_name', 'email', 'celular')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email', 'celular', 'correo_de_respaldo')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Roles Adicionales', {'fields': ('tipo_usuario',)}), 
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'password2')}
        ),
    )

    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)