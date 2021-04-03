from django.core.management.base import BaseCommand
from vipcontacts.vcard import import_in_vipcontacts
from os import listdir, chdir


class Command(BaseCommand):
    help = 'Import a vcard directory'

    def add_arguments(self, parser):
        parser.add_argument('--directory',  default=None, required=True)
        
    def handle(self, *args, **options):
        chdir(options['directory'])
        for filename in listdir(options["directory"]):
            import_in_vipcontacts(filename)

