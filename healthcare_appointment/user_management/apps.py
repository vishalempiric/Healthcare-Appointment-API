# user_management/apps.py

from django.apps import AppConfig

class UserManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_management'
    
    def ready(self):
        import user_management.signals  # Import signals module for registration
