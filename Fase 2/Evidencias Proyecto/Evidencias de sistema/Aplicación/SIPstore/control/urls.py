from django.urls import path
from . import views

urlpatterns = [
# !======================
# ! Iniciales 
# !======================
    path('control/',views.control, name='control'),
    path('stock/',views.stock, name='stock'),
    path('pedidos/',views.pedidos, name='pedidos'),
    path('pedidos/detail/<int:pk>/', views.pedido_detail, name='pedido_detail'),
# !======================
# ! Crear 
# !======================
    path('categoria/nueva/', views.crear_categoria, name='crear_categoria'),
    path('panel/nuevo/', views.crear_panel, name='crear_panel'),
    path('kit/nuevo/', views.crear_kit, name='crear_kit'),
    path('local/nuevo/', views.crear_local, name='crear_local'),
# !======================
# ! Editar
# !======================
    path('editar-categoria/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('editar-panel/<int:pk>/', views.editar_panel, name='editar_panel'),
    path('editar-kit/<int:pk>/', views.editar_kit, name='editar_kit'),
    path('editar-local/<int:pk>/', views.editar_local, name='editar_local'),
# !======================
# ! Eliminar
# !======================
    path('categoria/eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('panel/eliminar/<int:pk>/', views.eliminar_panel, name='eliminar_panel'),
    path('kit/eliminar/<int:pk>/', views.eliminar_kit, name='eliminar_kit'),
    path('local/eliminar/<int:pk>/', views.eliminar_local, name='eliminar_local'),
# !======================
# ! Imagenes
# !======================
    path('panel/<int:panel_id>/subir-imagenes/', views.subir_imagenes_panel, name='subir_imagenes_panel'),
    path('kit/<int:kit_id>/subir-imagenes/', views.subir_imagenes_kit, name='subir_imagenes_kit'),
    path('panel/<int:panel_id>/eliminar_imagenes/', views.eliminar_imagenes_panel, name='eliminar_imagenes_panel'),
    path('kit/<int:kit_id>/eliminar_imagenes/', views.eliminar_imagenes_kit, name='eliminar_imagenes_kit'),
# !======================
# ! Otras funciones
# !======================
    path('pedido/<int:pedido_id>/boleta/', views.descargar_boleta, name='descargar_boleta'),
    path('pedido/<int:pedido_id>/cambiar_estado/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
]