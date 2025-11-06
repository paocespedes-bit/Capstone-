# !Configuracion global de Las urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls), #!despues desabilitar
    path('', include('core.urls')),
    path('', include('store.urls')),
    path('', include('control.urls')),
    path('', include('cart.urls')),
    path('quote/',include('quote.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)