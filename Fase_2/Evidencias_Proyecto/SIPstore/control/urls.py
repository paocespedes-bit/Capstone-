from django.urls import path
from . import views

urlpatterns = [
    path('control/',views.control, name='control'),
    path('stock/',views.stock, name='stock'),
    path('categoria/nueva/', views.crear_categoria, name='crear_categoria'),
    path('panel/nuevo/', views.crear_panel, name='crear_panel'),
    path('kit/nuevo/', views.crear_kit, name='crear_kit'),
    path('categoria/eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('panel/eliminar/<int:pk>/', views.eliminar_panel, name='eliminar_panel'),
    path('kit/eliminar/<int:pk>/', views.eliminar_kit, name='eliminar_kit'),
    path('editar-categoria/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('editar-panel/<int:pk>/', views.editar_panel, name='editar_panel'),
    path('editar-kit/<int:pk>/', views.editar_kit, name='editar_kit'),
]