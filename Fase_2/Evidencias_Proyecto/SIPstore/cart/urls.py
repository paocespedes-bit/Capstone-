from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.carrito, name="carrito"),
    path('agregar/', views.agregar_producto, name='add'),
    path('eliminar/', views.eliminar_producto, name='del'),
    path('restar/', views.restar_producto, name='sub'),
    path('limpiar/', views.limpiar_carrito, name='cls'),
    ]