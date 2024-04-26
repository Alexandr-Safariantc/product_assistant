import os

from django.conf import settings
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Describe custom Django commands."""

    help = 'Create superuser from env variables if not exists.'

    def handle(self, *args, **options):
        """Create superuser from env variables if not exists."""
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username=os.getenv('DJANGO_SUPERUSER_USERNAME'),
                email=os.getenv('DJANGO_SUPERUSER_EMAIL'),
                password=os.getenv('DJANGO_SUPERUSER_PASSWORD')
            )
            self.stdout.write(
                self.style.SUCCESS(settings.SUPERUSER_CREATE_SUCCESS)
            )
        else:
            self.stdout.write(
                self.style.WARNING(settings.SUPERUSER_EXISTS_WARNING)
            )
