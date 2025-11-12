from django.urls import path, include  
from . import views

urlpatterns = [
    path('paneles/', views.paneles, name="paneles"),
    path('kits/', views.kits, name="kits"),
    path('kits/', views.kits, name="kits"),
    path('kits/<int:pk>/', views.kit_detail, name="kit_detail"),
    path('paneles/<int:pk>/', views.paneles_detail, name="paneles_detail"),
    path('coment/', include('coment.urls')),
]
