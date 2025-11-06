from django.urls import path
from . import views

urlpatterns=[
    path('', views.quote, name='quote' ),
    path("save_temp_form/", views.save_form, name="save_temp_form"),
    path("calcular_materiales/", views.calcular_materiales, name="calcular_materiales"),
    path("limpiar_calculo/", views.limpiar_calculo, name="limpiar_calculo"),
    
]