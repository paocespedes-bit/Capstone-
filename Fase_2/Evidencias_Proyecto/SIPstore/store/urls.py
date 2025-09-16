# !configuracion URL de store APP
from django.urls import path
from . import views

urlpatterns = [
    path('paneles/', views.paneles, name="paneles"),
    path('kits/',views.kits,name="kits")
    
]