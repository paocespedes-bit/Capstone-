from django.contrib import admin
from django.apps import apps

modelos = apps.get_app_config('store').get_models()

for modelo in modelos:
    try:
        admin.site.register(modelo)
    except admin.site.AlreadyRegistered:
        pass

# Register your models here.
