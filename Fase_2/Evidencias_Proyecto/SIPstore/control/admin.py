from django.contrib import admin
from .models import Local, Pedido, DetallePedido

# Inline para DetallePedido
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1
    readonly_fields = ('subtotal',)
    fields = ('content_type', 'object_id', 'cantidad', 'precio_unitario', 'subtotal')
    show_change_link = True

# Admin de Local
@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'telefono')
    search_fields = ('nombre', 'ubicacion')

# Admin de Pedido
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'comprador', 'local', 'estado', 'monto_total', 'fecha_pedido', 'fecha_retiro')
    list_filter = ('estado', 'fecha_pedido', 'local')
    search_fields = ('comprador', 'rut_cli', 'correo_cli')
    inlines = [DetallePedidoInline]
