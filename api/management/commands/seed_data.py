from django.core.management.base import BaseCommand
from api.models import Roles

class Command(BaseCommand):
    help = 'Seed initial data for Roles model'

    def handle(self, *args, **kwargs):
        roles = [{"id": 1, "name": 'Admin'}, {"id": 2, "name": 'User'}, {"id": 3, "name": 'Supplier'}]
        for role in roles:
            Roles.objects.update_or_create(id=role['id'], defaults={'name': role['name']})
        self.stdout.write(self.style.SUCCESS('Successfully seeded Roles data.'))