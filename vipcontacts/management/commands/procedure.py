from django.core.management.base import BaseCommand
from os import system
from vipcontacts.__init__ import __version__, __versiondatetime__

class Command(BaseCommand):
    help = 'New release procedure'

    def handle(self, *args, **options):
    
        print(f"Updating versions of vipcontacts frontend project to {__version__} and {__versiondatetime__}")
        system (f"""sed -i '3s/.*/  "version": "{__version__}",/' ../vipcontacts/package.json""")
        system (f"""sed -i '18s/.*/    version: "{__version__}",/' ../vipcontacts/src/main.js""")
        system (f"""sed -i '19s/.*/    versiondate: new Date({__versiondatetime__.strftime("%Y, %m, %d, %H, %M").replace(', 0', ', ')}),/' ../vipcontacts/src/main.js""")

        print()
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

