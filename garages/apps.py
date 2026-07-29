from django.apps import AppConfig
from django.db.models.signals import post_migrate

def auto_seed_on_migrate(sender, **kwargs):
    from django.conf import settings
    from garages.seeder import seed_global_parking_data
    if not settings.DEBUG:
        try:
            seed_global_parking_data()
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Auto-seed on migrate skipped or failed: {e}")

class GaragesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'garages'

    def ready(self):
        post_migrate.connect(auto_seed_on_migrate, sender=self)

