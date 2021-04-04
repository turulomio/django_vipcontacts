from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from vipcontacts.models import Person, Alias, Address,  RelationShip,  Log, Phone, Mail, Search
from vipcontacts.serializers import PersonSerializer, AliasSerializer, AddressSerializer, RelationShipSerializer, LogSerializer, PhoneSerializer, MailSerializer, PersonSerializerSearch, SearchSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]  

class AliasViewSet(viewsets.ModelViewSet):
    queryset = Alias.objects.all()
    serializer_class = AliasSerializer
    permission_classes = [permissions.IsAuthenticated] 
    
class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [permissions.IsAuthenticated] 
    
class RelationShipViewSet(viewsets.ModelViewSet):
    queryset = RelationShip.objects.all()
    serializer_class = RelationShipSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]

class PhoneViewSet(viewsets.ModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    permission_classes = [permissions.IsAuthenticated]

class SearchViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
    permission_classes = [permissions.IsAuthenticated]

class MailViewSet(viewsets.ModelViewSet):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
def login(request):
    print(request.POST.get("username"),  request.POST.get("password"))
    try:
        user=User.objects.get(username=request.POST.get("username"))
    except User.DoesNotExist:
        return Response("Invalid user")
        
    password=request.POST.get("password")
    pwd_valid=check_password(password, user.password)
    if not pwd_valid:
        return Response("Wrong password")

    if Token.objects.filter(user=user).exists():#Lo borra
        token=Token.objects.get(user=user)
        token.delete()
    token=Token.objects.create(user=user)
    return Response(token.key)
    
@api_view(['POST'])
def logout(request):
    print(request.POST.get("key"))
    token=Token.objects.get(key=request.POST.get("key"))
    if token is None:
        return Response("Invalid token")
    else:
        token.delete()
        return Response("Logged out")

@csrf_exempt
@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, ])
def person_find(request):
    search=request.GET.get("search", "__none__")
    if search=="__none__":
        qs=Person.objects.none()
    elif search=="__all__":
        qs=Person.objects.all()
    else:
        qs_search=Search.objects.all().filter(string__icontains=search)
        person_ids=[s.person.id for s in qs_search]
        qs=Person.objects.all().filter(id__in=person_ids).distinct()

    serializer = PersonSerializerSearch(qs, many=True, context={'request': request} )
    return JsonResponse(serializer.data, safe=False)

