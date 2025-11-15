from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import (
    Categoria,
    KitConstruccion,
    PanelSIP,
    imagenProducto,
    Oferta,
    Comentario,
    Inventario,
    Resena
)

class ImagenProductoInline(GenericTabularInline):
    model = imagenProducto
    extra = 1

class InventarioInline(GenericTabularInline):
    model = Inventario
    extra = 1         
    max_num = 1       
    min_num = 1       
    ct_field = "content_type"
    ct_fk_field = "object_id"
    fields = ('disponible', 'reservado', 'modo_stock')
    verbose_name = "Inventario"
    verbose_name_plural = "Inventario"
    can_delete = False 
    
# Personalización para el modelo KitConstruccion
@admin.register(KitConstruccion)
class KitConstruccionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'm2', 'dormitorios', 'banos', 'precio_actual')
    # Permite buscar por nombre y descripción
    search_fields = ('nombre', 'descripcion')
    # Permite filtrar por categorías
    list_filter = ('categorias',)
    # Muestra las imágenes en la misma página de edición del kit
    inlines = [ImagenProductoInline,InventarioInline]
    # Muestra los campos en el orden especificado
    fields = ('nombre', 'precio', 'descripcion', 'm2', 'dormitorios', 'banos', 'categorias')

# Personalización para el modelo PanelSIP
@admin.register(PanelSIP)
class PanelSIPAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'espesor', 'largo', 'ancho', 'precio_actual')
    search_fields = ('nombre', 'tipo_obs', 'madera_union')
    list_filter = ('categorias',)
    inlines = [ImagenProductoInline,InventarioInline]

# Registro de los modelos restantes, también se puede usar el decorador @admin.register()
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'precio_oferta', 'porcentaje_dcto', 'fecha_inicio', 'fecha_fin')
    list_filter = ('fecha_inicio', 'fecha_fin')
    search_fields = ('producto__nombre',) 

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'producto', 'estrellas', 'fecha_comentario')
    list_filter = ('estrellas', 'fecha_comentario')
    search_fields = ('autor', 'texto', 'producto__nombre')

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('autor', 'texto', 'fecha_comentario', 'revisado')
    list_filter = ('revisado', 'fecha_comentario')
    search_fields = ('autor', 'texto')
    list_editable = ('revisado',)  # Para editar desde la lista