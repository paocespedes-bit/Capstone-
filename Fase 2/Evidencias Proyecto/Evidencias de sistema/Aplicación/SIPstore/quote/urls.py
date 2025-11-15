from django.urls import path
from . import views

urlpatterns=[
    path('', views.quote, name='quote' ),
    path("save_temp_form/", views.save_form, name="save_temp_form"),
    path("calcular_materiales/", views.calcular_materiales, name="calcular_materiales"),
    path("limpiar_calculo/", views.limpiar_calculo, name="limpiar_calculo"),
    path("descargar_cotizacion/<str:formato>/", views.descargar_cotizacion, name="descargar_cotizacion"),
    path('agregar-al-carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path("enviar-cotizacion/", views.enviar_cotizacion, name="enviar_cotizacion"),
]