from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db.models import Case, When
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets,  status, permissions
from vipcontacts.reusing.connection_dj import cursor_one_column, cursor_rows, execute
from vipcontacts.models import Person, Alias, Address,  RelationShip, Job, Log, Phone, Mail, Search, Group, person_from_person_url, Blob
from vipcontacts.serializers import PersonSerializer, AliasSerializer, AddressSerializer, RelationShipSerializer, JobSerializer, GroupSerializer, LogSerializer, PhoneSerializer, MailSerializer, PersonSerializerSearch, SearchSerializer,  BlobSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _ #With gettext it doesn't work onky with gettext_lazy. Reason?

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
class BlobViewSet(viewsets.ModelViewSet):
    queryset = Blob.objects.all()
    serializer_class = BlobSerializer
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
def person_find_last_editions(request):
    limit=int(request.GET.get("limit", "30"))
    person_ids=cursor_one_column("""
        select 
            persons.id, 
            max(logs.datetime) 
        from 
            persons, 
            logs 
        where 
            persons.id=logs.person_id 
        group by 
            persons.id 
        order by 
            max(logs.datetime) desc
        limit %s""", (limit, ))
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(person_ids)])
    qs=Person.objects.all().filter(id__in=person_ids).order_by(preserved)
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
    for o in qs:
        r.append({"organization": o["organization"]})
    return JsonResponse(r, safe=False)



    
    
    
@csrf_exempt
@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, ])
def blob_names(request):
    search=request.GET.get("search", "__none__")
    if search=="__none__":
        qs=Blob.objects.none()
    elif search=="__all__":
        qs=Blob.objects.values('name').distinct()
    else:
        qs=Blob.objects.values('name').distinct().filter(name__icontains=search).order_by()

    r=[]
    for o in qs:
        r.append({"name": o["name"]})
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
    
    

@csrf_exempt
@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, ])
def group_members(request):
    search=request.GET.get("search", "__none__")
    members=request.GET.get("members",  "true")
    if search=="__none__":
        qs=Person.objects.none()
    else:
        qs_search=Group.objects.all().filter(name=search)
        person_ids=[s.person.id for s in qs_search]
        if members=="true":
            qs=Person.objects.all().filter(id__in=person_ids).distinct()
        else:
            qs=Person.objects.all().exclude(id__in=person_ids).distinct()

    serializer = PersonSerializerSearch(qs, many=True, context={'request': request} )
    return JsonResponse(serializer.data, safe=False)
        

@csrf_exempt
@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, ])
def statistics(request):
    r=[]
    for name, cls in ((_("Contacts"), Person), (_("Jobs"), Job), (_("Mails"), Mail), (_("Phones"), Phone),  (_("Relations"), RelationShip), (_("Alias"), Alias), (_("Addresses"), Address), (_("Groups"), Group), (_("Media"),  Blob)):
        r.append({"name": name, "value":cls.objects.all().count()})
    return JsonResponse(r, safe=False)
    

@csrf_exempt
@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, ])
def group_members_full(request):
    search=request.GET.get("search", "__none__")
    members=request.GET.get("members",  "true")
    if search=="__none__":
        qs=Person.objects.none()
    else:
        qs_search=Group.objects.all().filter(name=search)
        person_ids=[s.person.id for s in qs_search]
        if members=="true":
            qs=Person.objects.all().filter(id__in=person_ids).distinct()
        else:
            qs=Person.objects.all().exclude(id__in=person_ids).distinct()

    serializer = PersonSerializer(qs, many=True, context={'request': request} )
    return JsonResponse(serializer.data, safe=False)
    
    
## Needs url and name get parameters
@csrf_exempt
@api_view(['DELETE', ])
@permission_classes([permissions.IsAuthenticated, ])
def delete_group_by_name(request):
    person_url=request.GET.get("url", None)
    group_name=request.GET.get("name", None)
    if person_url is None or group_name is None:
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    person=person_from_person_url(person_url)
    qs_groups=Group.objects.filter(person=person, name=group_name)
    number=len(qs_groups)
    qs_groups.delete()
    person.update_search_string()
    return Response(f"Deleted: {number}")


    
@csrf_exempt
@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, ])
## Busca cadenas distintas en table field
## Si find necesita replace, para unir y para renombrar.
## Si ninguno de los dos consulta un distinct
def merge_text_fields(request, table, field):
    find=request.GET.getlist("find", None)
    replace=request.GET.get("replace", None)
    
    if find is None or replace is None:
        rows=cursor_rows(f"select count(*), {field} as name from {table} where {field} is not null and {field}!=''  group by {field}")
        return JsonResponse(rows, safe=False)
    else:
        execute(f"update {table} set {field}=%s where {field} in %s", (replace, tuple(find)))
        ## Update search strings
        ids_contacts_updated=cursor_one_column(f"select person_id from {table} where {field}=%s", (replace, ))
        for p in Person.objects.all().filter(id__in=ids_contacts_updated):
            p.update_search_string()
    
        return JsonResponse(True,safe=False)
    

#    
#    
#from django.http import HttpResponse
#@csrf_exempt
#@transaction.atomic
#@api_view(['POST', ])
#@permission_classes([permissions.IsAuthenticated, ])
#def blob_post(request):
#    form = BlobPost(request.POST)
#    if "blob" not in request.FILES:
#        return HttpResponse("You need to post a file")
#    else:
#        blob = request.FILES["blob"]
#        print(blob)
#        print(blob.__class__)
#        print(dir(blob))
#    
#    if form.is_valid():
#        print(form.cleaned_data)
#        form.cleaned_data['blob']=blob.read()
#        form.cleaned_data['person']=person_from_person_url(form.cleaned_data['person'])
#        b=Blob(**form.cleaned_data)
#        b.save()
#        return HttpResponse("Blob posted")
#    else:
#        print(form.errors)
#        return HttpResponse(form.errors)
    
#    
#@csrf_exempt
#@transaction.atomic
#@permission_classes([permissions.IsAuthenticated, ])
#def blob_get(request, pk):
#    if request.method == 'POST':
#        form = BlobPost(request.POST)
#        if "blob" not in request.FILES:
#            return HttpResponse("You need to post a file")
#        else:
#            blob = request.FILES["blob"]
#            print(blob)
#            print(blob.__class__)
#            print(dir(blob))
#        
#        if form.is_valid():
#            print(form.cleaned_data)
#            form.cleaned_data['blob']=blob.read()
#            form.cleaned_data['person']=person_from_person_url(form.cleaned_data['person'])
#            b=Blob(**form.cleaned_data)
#            b.save()
#            return HttpResponse("Blob posted")
#        else:
#            print(form.errors)
#            return HttpResponse(form.errors)
#    return HttpResponse("Should be only POST")
