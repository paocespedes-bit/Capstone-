from django.contrib import admin
from .models import Local, Pedido, DetallePedido

# Inline para DetallePedido
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1
    fields = ('content_type', 'object_id', 'cantidad', 'get_precio', 'get_subtotal')
    readonly_fields = ('get_precio', 'get_subtotal')
    show_change_link = True

    def get_precio(self, obj):
        return obj.precio_unitario
    get_precio.short_description = "Precio Unitario"

    def get_subtotal(self, obj):
        return obj.subtotal
    get_subtotal.short_description = "Subtotal"

# Admin de Local
@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'telefono')
    search_fields = ('nombre', 'ubicacion')

# Admin de Pedido
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'comprador', 'local', 'estado', 'monto_total', 'fecha_pedido', 'fecha_retiro','metodo_pago' )
    list_filter = ('estado', 'fecha_pedido', 'local', 'metodo_pago')
    search_fields = ('comprador', 'rut_cli', 'correo_cli')
    inlines = [DetallePedidoInline]
