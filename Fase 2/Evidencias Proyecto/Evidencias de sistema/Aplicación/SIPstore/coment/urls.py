from django.urls import path
from . import views

urlpatterns = [
    path('<str:app_label>/<str:model_name>/<int:producto_id>/', views.calificar_producto, name='calificar_producto'),
]

