from argparse import ArgumentParser
from vipcontacts.reusing.github import download_from_github
from os import remove

def replace_in_file(filename, s, r):
    data=open(filename,"r").read()
    remove(filename)
    data=data.replace(s,r)
    f=open(filename, "w")
    f.write(data)
    f.close()

parser=ArgumentParser()
parser.add_argument('--local', help='Parses files without download', action="store_true", default=False)
args=parser.parse_args()      

if args.local==False:
    download_from_github("turulomio", "reusingcode", "django/connection_dj.py", "vipcontacts/reusing")
    download_from_github("turulomio", "reusingcode", "python/casts.py", "vipcontacts/reusing")
    download_from_github("turulomio", "reusingcode", "python/decorators.py", "vipcontacts/reusing")
    download_from_github("turulomio", "reusingcode", "python/datetime_functions.py", "vipcontacts/reusing")
    download_from_github("turulomio", "reusingcode", "python/listdict_functions.py", "vipcontacts/reusing")
    download_from_github("turulomio", "reusingcode", "python/github.py", "vipcontacts/reusing")
    download_from_github("turulomio", "reusingcode", "django/request_casting.py", "vipcontacts/reusing")
    download_from_github("turulomio", "reusingcode", "django/responses_json.py", "vipcontacts/reusing")
    download_from_github("turulomio", "django_moneymoney", "moneymoney/views_login.py", "vipcontacts/reusing")


replace_in_file("vipcontacts/reusing/views_login.py", "moneymoney.reusing", "")
