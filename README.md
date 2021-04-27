# django_vipcontacts

Django project that serves an API to VipContacts (https://github.com/turulomio/vipcontacts) to manage your contacts in a different way

## Links

Doxygen documentation:
    http://turulomio.users.sourceforge.net/doxygen/django_vipcontacts/

Github web page:
    https://github.com/turulomio/django_vipcontacts/

## Dependencies

* Django
* Django rest frameworkds
* Django CORS headers

## Issues

If you have any issues with this project, please report then in the frontend project https://github.com/turulomio/vipcontacts/issues

## Installation
### Using python manage.py runserver

1) Install following packages with pip
```
    pip install django-cors-headers
    pip install djangorestframework
```
2) Change your database settings pointing to a new database in django_vipcontacts/settings.py
3) Create your database ( I use postgres, the rest of databases hasn't been tested )
4) Clone this project and enter main directory
5) `python manage.py migrate`
6) `python manage.py runserver 8002`
7) `python manage.py createsuperuser`
8) Open http://127.0.0.1:8002/ in your browser and you'll see Vip Contacts API. You can change ports but you'll have to configure both frontend and backend CORS settings

NOW YOU HAVE TO INSTALL VIPCONTACTS FROM (https://github.com/turulomio/vipcontacts)

## Changelog

### 0.3.0 (2021-04-23)
- Added chips to search model
- Added more relation types
- Added more necessary views
