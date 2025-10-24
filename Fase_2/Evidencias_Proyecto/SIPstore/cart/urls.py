from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.carrito, name="carrito"),
    path('agregar/', views.agregar_producto, name="add_ajax"),
    path('modificar/<str:accion>/', views.modificar_carrito, name="modificar_ajax" ),
    path('crear-pedido/', views.crear_pedido, name='crear_pedido'),
    path('confirmacion-pago/<int:pk>/', views.confirm_pago, name='confirm_pago'),
    ]