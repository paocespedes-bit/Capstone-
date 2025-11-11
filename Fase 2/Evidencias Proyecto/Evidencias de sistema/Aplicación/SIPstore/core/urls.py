# !configuracion URL de store APP
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    
]