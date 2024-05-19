from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "Create a superuser account"

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                first_name="admin",
                last_name="admin",
                username="admin",
                phone_number="+380998887766",
                email="admin@admin.com",
                password="admin",
                role=[User.ADMIN],
            )
            self.stdout.write(self.style.SUCCESS("Superuser created successfully"))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists"))
