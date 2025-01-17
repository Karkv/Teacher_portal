# schedules/apps.py

from django.apps import AppConfig

class SchedulesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'schedules'

    def ready(self):
        import schedules.signals  # Import signals to automatically create Teacher instances
