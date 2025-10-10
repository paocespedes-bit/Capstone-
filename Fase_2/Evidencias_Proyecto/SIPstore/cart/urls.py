from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.carrito, name="carrito"),
    path("agregar_carrito/", views.agregar_carrito, name="agregar_carrito"),
    path("vaciar-carrito/", views.vaciar_carrito, name="vaciar_carrito"),
]