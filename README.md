# django_vipcontacts

## Links

Doxygen documentation:
    http://turulomio.users.sourceforge.net/doxygen/django_vipcontacts/

Github web page:
    https://github.com/turulomio/django_vipcontacts/

Pypi web page:
    https://pypi.org/project/xulpymoney/

## Dependencies

* Django
* Django rest frameworkds
* Django CORS headers

## How to check API

To check api from console:

GET 

`curl -H 'Accept: application/json; indent=4' -u user:pass http://127.0.0.1:8001/api/persons/`

POST

`curl -X POST -d 'username=user' -d 'password=pass' http://127.0.0.1:8001/login`
`curl -H 'Authorization: Token 2132e2622c136bc59b6bcd732df2ca1cabadca4c'  http://192.168.1.100:8001/api/persons/`

## Changelog

### 0.3.0 (2021-04-23)
- Added chips to search model
- Added more relation types
- Added more necessary views
