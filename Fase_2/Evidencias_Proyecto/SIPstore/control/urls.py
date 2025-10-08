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
    path('panel/<int:panel_id>/subir-imagenes/', views.subir_imagenes_panel, name='subir_imagenes_panel'),
    path('eliminar-imagen/<int:imagen_id>/', views.eliminar_imagen, name='eliminar_imagen'),
    path('kit/<int:kit_id>/subir-imagenes/', views.subir_imagenes_kit, name='subir_imagenes_kit'),
    path("kit/eliminar-imagen/<int:imagen_id>/", views.eliminar_imagen_kit, name="eliminar_imagen_kit"),
    path('pedidos/',views.pedidos, name='pedidos'),
    path('pedidos/detail/',views.pedido_detail, name='pedido_detail'),
]