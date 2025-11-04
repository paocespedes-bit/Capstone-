from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.carrito, name="carrito"),
    path('agregar/', views.agregar_producto, name="add_ajax"),
    path('modificar/<str:accion>/', views.modificar_carrito, name="modificar_ajax" ),
    path('crear-pedido/', views.crear_pedido, name='crear_pedido'),
    
    path('crear_preferencia/', views.crear_preferencia, name='crear_preferencia'),
    path('pago_exitoso/<int:pedido_id>/', views.pago_exitoso, name='pago_exitoso'),
    path('pago_fallido/', views.pago_fallido, name='pago_fallido'),
    path('pago_pendiente/<int:pedido_id>/', views.pago_pendiente, name='pago_pendiente'),
    

    ]