from money.connection_dj import cursor_rows
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Command to dump database translatable string to hardcoded_strings.py'

    def handle(self, *args, **options):
        f=open("vipcontacts/hardcoded_strings.py", "w")
        f.write("from django.utils.translation import ugettext_lazy as _\n")
        for row in cursor_rows("select name from groups where editable is false order by name"):
            f.write("_('{}')\n".format(row["name"]))
        f.close()

