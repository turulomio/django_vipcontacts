from django.core.management.base import BaseCommand
from vipcontacts.vcard import import_in_vipcontacts


class Command(BaseCommand):
    help = 'Import a vcard file'

    def add_arguments(self, parser):
        parser.add_argument('--file',  default=None, required=True)
        
    def handle(self, *args, **options):
        person=import_in_vipcontacts(options["file"])
        print(f"VCard '{options['file']}' imported: {str(person)}")
