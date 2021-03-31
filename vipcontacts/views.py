from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets,  permissions
from vipcontacts.models import Person, Alias, Address
from vipcontacts.serializers import PersonSerializer, AliasSerializer, AddressSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
#    permission_classes = [permissions.IsAuthenticated]  # SI QUITO AUTENTICACION PUEDO NAVEGAR POR LA URL DE DJANGO_REST

class AliasViewSet(viewsets.ModelViewSet):
    queryset = Alias.objects.all()
    serializer_class = AliasSerializer
#    permission_classes = [permissions.IsAuthenticated]  # SI QUITO AUTENTICACION PUEDO NAVEGAR POR LA URL DE DJANGO_REST
    

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
#    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        if len(self.request.GET)==0:#No get paramters:
            return viewsets.ModelViewSet.list(self, request)

        search=self.request.GET.get("search", "")
        #Filtering by search
        if search=="":
            qs=Person.objects.none()
        elif search=="*":
            qs=Person.objects.all()
        else:
            qs=Person.objects.filter(
                Q(name__icontains=search) | 
                Q(surname__icontains=search) | 
                Q(surname2__icontains=search)
            )
        serializer = PersonSerializer(qs, many=True)
        return Response(serializer.data)

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
