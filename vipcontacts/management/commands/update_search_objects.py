from django.core.management.base import BaseCommand
from vipcontacts.models import Person

class Command(BaseCommand):
    help = 'Updates all search objects from all contacts'

    def handle(self, *args, **options):
        qs=Person.objects.all()
        for p in Person.objects.all():
            p.update_search_string()
        print(f"Updated search objects from {len(qs)} contacts")
