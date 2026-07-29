from django.core.management.base import BaseCommand
from garages.seeder import seed_global_parking_data

class Command(BaseCommand):
    help = 'Seeds global garage, slot, valet, company, service, and user data.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force seeding even if garages already exist in the database.',
        )

    def handle(self, *args, **options):
        force = options.get('force', False)
        self.stdout.write("Starting data seeding process...")
        created = seed_global_parking_data(force=force)
        if created:
            self.stdout.write(self.style.SUCCESS("Successfully seeded global parking data!"))
        else:
            self.stdout.write(self.style.WARNING("Database already contains garage data. Use --force to override."))
