from vipcontacts.reusing.github import download_from_github
from vipcontacts.reusing.file_functions import replace_in_file
from sys import argv
from os import system

def reusing():
    """
        Actualiza directorio reusing
        poe reusing
        poe reusing --local
    """
    local=False
    if len(argv)==2 and argv[1]=="--local":
        local=True
        print("Update code in local without downloading was selected with --local")
    if local==False:

        download_from_github("turulomio", "reusingcode", "django/connection_dj.py", "vipcontacts/reusing")
        download_from_github("turulomio", "reusingcode", "python/decorators.py", "vipcontacts/reusing")
        download_from_github("turulomio", "reusingcode", "python/file_functions.py", "vipcontacts/reusing")
        download_from_github("turulomio", "reusingcode", "python/github.py", "vipcontacts/reusing")
        download_from_github("turulomio", "django_moneymoney", "moneymoney/views_login.py", "vipcontacts/reusing")
        download_from_github("turulomio", "django_calories_tracker", "calories_tracker/tests_helpers.py", "vipcontacts/reusing")

    replace_in_file("vipcontacts/reusing/views_login.py", "moneymoney.reusing", "")

def cypress_test_server():
    print("- Dropping test_xulpymoney database...")
    system("dropdb -U postgres -h 127.0.0.1 test_vipcontacts")
    print("- Launching python manage.py test_server with user 'test' and password 'test'")
    system("python manage.py testserver vipcontacts/fixtures/test_server.json --addrport 8002")
