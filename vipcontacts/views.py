from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets,  status, permissions
from vipcontacts.models import Person, Alias, Address,  RelationShip, Job, Log, Phone, Mail, Search, Group
from vipcontacts.serializers import PersonSerializer, AliasSerializer, AddressSerializer, RelationShipSerializer, JobSerializer, GroupSerializer, LogSerializer, PhoneSerializer, MailSerializer, PersonSerializerSearch, SearchSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete_log()
        instance.person.update_search_string()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AliasViewSet(viewsets.ModelViewSet):
    queryset = Alias.objects.all()
    serializer_class = AliasSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete_log()
        instance.person.update_search_string()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete_log()
        instance.person.update_search_string()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated] 
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete_log()
        instance.person.update_search_string()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [permissions.IsAuthenticated] 
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete_log()
        instance.person.update_search_string()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class RelationShipViewSet(viewsets.ModelViewSet):
    queryset = RelationShip.objects.all()
    serializer_class = RelationShipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete_log()
        instance.person.update_search_string()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]

class PhoneViewSet(viewsets.ModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete_log()
        instance.person.update_search_string()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SearchViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
    permission_classes = [permissions.IsAuthenticated]

class MailViewSet(viewsets.ModelViewSet):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete_log()
        instance.person.update_search_string()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
    
@csrf_exempt
@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, ])
def person_get_relationship_fullnames(request, person_id):
    r=[]
    qs_relationships=RelationShip.objects.all().filter(person_id=person_id).select_related("person")
    for o in qs_relationships:
        r.append({"id": o.destiny.id, "name":o.destiny.fullName()})
    return JsonResponse(r, safe=False)
    
@csrf_exempt
@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, ])
def professions(request):    
    search=request.GET.get("search", "__none__")
    if search=="__none__":
        qs=Job.objects.none()
    elif search=="__all__":
        qs=Job.objects.values('profession').distinct()
    else:
        qs=Job.objects.values('profession').distinct().filter(profession__icontains=search).order_by()

    r=[]
    qs=Job.objects.order_by().values('profession').distinct()
    for o in qs:
        r.append({"profession": o["profession"]})
    return JsonResponse(r, safe=False)
    
    
@csrf_exempt
@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, ])
def organizations(request):
    search=request.GET.get("search", "__none__")
    if search=="__none__":
        qs=Job.objects.none()
    elif search=="__all__":
        qs=Job.objects.values('organization').distinct()
    else:
        qs=Job.objects.values('organization').distinct().filter(organization__icontains=search).order_by()

    r=[]
    qs=Job.objects.order_by().values('organization').distinct()
    for o in qs:
        r.append({"organization": o["organization"]})
    return JsonResponse(r, safe=False)

@csrf_exempt    
@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, ])
def departments(request):    
    search=request.GET.get("search", "__none__")
    if search=="__none__":
        qs=Job.objects.none()
    elif search=="__all__":
        qs=Job.objects.values('department').distinct()
    else:
        qs=Job.objects.values('department').distinct().filter(department__icontains=search).order_by()
    r=[]
    qs=Job.objects.order_by().values('department').distinct()
    for o in qs:
        r.append({"department": o["department"]})
    return JsonResponse(r, safe=False)

@csrf_exempt    
@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, ])
def titles(request):
    search=request.GET.get("search", "__none__")
    if search=="__none__":
        qs=Job.objects.none()
    elif search=="__all__":
        qs=Job.objects.values('title').distinct()
    else:
        qs=Job.objects.values('title').distinct().filter(title__icontains=search).order_by()
    r=[]
    qs=Job.objects.order_by().values('title').distinct()
    for o in qs:
        r.append({"title": o["title"]})
    return JsonResponse(r, safe=False)
    
@csrf_exempt    
@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, ])
def groups(request):
    search=request.GET.get("search", "__none__")
    if search=="__none__":
        qs=Group.objects.none()
    elif search=="__all__":
        qs=Group.objects.values('name').distinct()
    else:
        qs=Group.objects.values('name').distinct().filter(name__icontains=search).order_by()
    r=[]
    for o in qs:
        r.append({"name": o["name"]})
    return JsonResponse(r, safe=False)

