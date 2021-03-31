#!/usr/bin/python3
from subprocess import run

token='0000000000000000000000000000000000000000'
url="http://192.168.1.100:8001/api/persons"


print( "Change your active token")
print(f"update authtoken_token set key='{token}' where user_id=1")

print ("LISTAR TODO")
p=run(f"curl -H 'Authorization: Token {token}' -X GET {url}/", shell=True)

print("")
print ("LISTAR TIENEN ARIA")
p=run(f"curl -H 'Authorization: Token {token}' -X GET {url}/?search=aria", shell=True)


print ("")
print ("POST ADD PERSON")
p=run(f"""curl -d '{{"name":"Auto", "surname":"Auto", "surname2":"Auto", "birth": "1976-12-12", "death":null, "gender": 0}}' -H "Content-Type: application/json" -H "Authorization: Token {token}" -X POST {url}/""", shell=True, capture_output=True)
id=p.stdout.decode('UTF-8').split(",")[0].split(":")[1]

print(p.stdout)
print("UPDATE PERSON",id)
p=run(f"""curl -d '{{"name":"Autoupdate", "surname":"Autoupdate", "surname2":"Autoupdate", "birth": "1976-12-12", "death":null, "gender": 0}}' -H "Content-Type: application/json" -H "Authorization: Token {token}" -X PUT {url}/{id}/""", shell=True)

print("")
print ("GET ONE", id)
p=run(f"curl -H 'Authorization: Token {token}' -X GET {url}/{id}/", shell=True)

print("")
print("DELETE PERSON", id)
p=run(f"""curl  -H "Authorization: Token {token}" -X DELETE {url}/{id}/""", shell=True)
