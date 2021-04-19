from django.core.management.base import BaseCommand
from vipcontacts.__init__ import __version__

class Command(BaseCommand):
    help = 'New release procedure'

    def handle(self, *args, **options):
        print("Updating versions of vipcontacts frontend project")

        print(f"""To release a new version:
DJANGO_VIPCONTACTS
  * Change version and version date in vipcontacts.__init__.py
  * Add release changelog en README.md
  * python manage.py makemessages
  * linguist
  * python manage.py compilemessages
  * python manage.py doxygen
  * git commit -a -m 'django_vipcontacts-{__version__}'
  * git push
  * Hacer un nuevo tag en GitHub de django_vipcontacts

VIPCONTACTS
  * Cambiar a vipcontacts project
  * Add release changelog in README.md
  * git commit -a -m 'vipcontacts-{__version__}'
  * git push
  * Hacer un nuevo tag en GitHub de vipcontacts
""")

