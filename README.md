# django_vipcontacts

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
