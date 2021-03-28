from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets,  permissions

from vipcontacts.models import Person
from vipcontacts.serializers import PersonSerializer

class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Person.objects.all().order_by('name')
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        search=self.request.GET.get("search", "")
        if search=="":
            return self.queryset.none()
        if search=="*":
            return self.queryset
        return self.queryset.filter(
            Q(name__icontains=search) | 
            Q(surname__icontains=search) | 
            Q(surname2__icontains=search)
        )


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
