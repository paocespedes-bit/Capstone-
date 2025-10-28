from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.carrito, name="carrito"),
    path('agregar/', views.agregar_producto, name="add_ajax"),
    path('modificar/<str:accion>/', views.modificar_carrito, name="modificar_ajax" ),
    path('crear-pedido/', views.crear_pedido, name='crear_pedido'),
    path('confirmacion-pago/<int:pedido_id>/', views.confirm_pago, name='confirm_pago'),
    path('info-pedido/', views.info_pedido, name='info_pedido'),
    path('confirmar-pago-manual/<int:pedido_id>/', views.confirmar_pago_manual, name='confirmar_pago_manual'),

    ]