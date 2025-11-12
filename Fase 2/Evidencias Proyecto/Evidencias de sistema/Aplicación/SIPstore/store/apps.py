from django.apps import AppConfig

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'  # 👈 debe coincidir exactamente con el nombre de la carpeta de la app

    def ready(self):
        import store.signals  # 👈 asegúrate de usar el mismo nombre que el archivo