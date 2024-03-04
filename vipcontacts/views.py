from datetime import date, timedelta
from django.db import transaction
from django.db.models import Subquery
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _ #With gettext it doesn't work onky with gettext_lazy. Reason?
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import viewsets,  status, permissions
from vipcontacts.reusing.connection_dj import cursor_one_column, cursor_rows, execute, show_queries, show_queries_function
from vipcontacts.reusing.decorators import ptimeit
from request_casting.request_casting import all_args_are_not_none, RequestString, RequestUrl
from vipcontacts.models import Person, PersonGender, Alias, Address,  RelationShip, Job, Log, Phone, Mail, Search, Group, person_from_person_url, Blob, get_country_name, LogType
from vipcontacts.serializers import PersonSerializer, AliasSerializer, AddressSerializer, RelationShipSerializer, JobSerializer, GroupSerializer, LogSerializer, PhoneSerializer, MailSerializer, PersonSerializerSearch, SearchSerializer,  BlobSerializer

show_queries_function
show_queries
ptimeit

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]  

class AliasViewSet(viewsets.ModelViewSet):
    queryset = Alias.objects.all()
    serializer_class = AliasSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.person.update_search_string()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.person.update_search_string()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated] 
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
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
        instance.person.update_search_string()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.prefetch_related("mail").prefetch_related("phone").prefetch_related("search").prefetch_related("alias").prefetch_related("job").prefetch_related("group").prefetch_related("blob").prefetch_related("address").prefetch_related("relationship").prefetch_related("log").all()
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    ## ?search=                 To search a string
    
    def list(self, request):
        """
            :LAST 40        Shows last edited records
        """
        search=RequestString(self.request,"search")
        if all_args_are_not_none(search):
            if search.lower()=="__none__":
                self.queryset=self.queryset.none()
            elif search.startswith(":LAST "):
                try:
                    last_editions=int(search.split(" ")[1])
                except:
                    last_editions=40
                self.queryset=self.queryset.order_by("-dt_update")[:last_editions]
            elif search.lower()=="__all__":
                self.queryset=self.queryset
            else:
                qs_search=Search.objects.select_related("person").filter(string__icontains=search.lower())
                self.queryset=self.queryset.filter(id__in=Subquery(qs_search.values("person__id")))
        serializer = PersonSerializer(self.queryset, many=True, context={'request': request})
        return Response(serializer.data)
        
    @action(detail=True, methods=["get"], name='Returns historical register', url_path="historical_register", url_name='historical_register', permission_classes=[permissions.IsAuthenticated])
    def historical_register(self, request, pk=None):
        person= self.get_object()
        r=Person.historical_register(person.id)
        return Response(r)
        
    
class PhoneViewSet(viewsets.ModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
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
        instance.person.update_search_string()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, ])
def person_get_relationship_fullnames(request, person_id):
    r=[]
    qs_relationships=RelationShip.objects.all().filter(person_id=person_id).select_related("person")
    for o in qs_relationships:
        r.append({"id": o.destiny.id, "name":o.destiny.fullName()})
    return JsonResponse(r, safe=False)
    

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
        

@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, ])
def statistics(request):
    r={}
    r["registers"]=[]
    for name, cls in ((_("Contacts"), Person), (_("Jobs"), Job), (_("Mails"), Mail), (_("Phones"), Phone),  (_("Relations"), RelationShip), (_("Alias"), Alias), (_("Addresses"), Address), (_("Groups"), Group), (_("Media"),  Blob)):
        r["registers"].append({"name": name, "value":cls.objects.all().count()})
        
    r["gender"]=[]
    for row in cursor_rows("select count(*) as value, gender from persons group by gender"):
        r["gender"].append({"name": PersonGender.get_label(row['gender']), "value":row["value"]})     
        
    r["jobs"]=[]
    for row in cursor_rows("select count(*) as value, profession as name from jobs group by profession"):
        if not ( row["name"] is None or row["name"]==""):
            r["jobs"].append(row)
            
    r["countries"]=[]
    for row in cursor_rows("select count(*) as value, country as name from addresses group by country"):

        r["countries"].append({"name": get_country_name(row['name']), "value":row["value"]})     

    r["cities"]=[]
    for row in cursor_rows("select count(*) as value, city as name from addresses group by city"):
        if not ( row["name"] is None or row["name"]==""):
            r["cities"].append(row)


    return JsonResponse(r, safe=False)
    


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
    



@api_view(['POST'])    
@permission_classes([permissions.IsAuthenticated, ])
@transaction.atomic
def PersonsMerge(request):
    person_from=RequestUrl(request, "from", Person)
    person_to=RequestUrl(request, "to", Person)
    
    if all_args_are_not_none(person_from, person_to):
        Address.objects.filter(person=person_from).update(person=person_to)
        Alias.objects.filter(person=person_from).update(person=person_to)
        Blob.objects.filter(person=person_from).update(person=person_to)
        Group.objects.filter(person=person_from).update(person=person_to)
        Job.objects.filter(person=person_from).update(person=person_to)
        Log.objects.filter(person=person_from).update(person=person_to)
        Mail.objects.filter(person=person_from).update(person=person_to)
        Phone.objects.filter(person=person_from).update(person=person_to)
        RelationShip.objects.filter(person=person_from).update(person=person_to)
        person_to.update_search_string(request)
        
        person_from.delete()
        l=Log(datetime=timezone.now(), person=person_to, retypes=LogType.ContactMerge, text=f"{person_from} => {person_to}")
        l.save()    
        return JsonResponse(True,safe=False)
    

    return JsonResponse(False,safe=False)
    
@api_view(['GET'])    
@permission_classes([permissions.IsAuthenticated, ])
def NextImportantDates(request):
    ## Appends a qs of persons with a reason
    def append(r, qs, reason, attribute):
        
        for p in qs:
            r.append({
                "person": p.fullName(), 
                "id": p.id, 
                "url": request.build_absolute_uri(reverse('person-detail', args=(p.pk, ))), 
                "reason": reason, 
                "date": getattr(p, attribute), 
            })
    ###
    r=[]

    
    qs=Person.objects.filter(birth__month=date.today().month, birth__day=date.today().day)
    append(r, qs, _("Birthdays"),  "birth")
        
    qs=Person.objects.filter(birth__month=(date.today()+timedelta(days=1)).month, birth__day=(date.today()+timedelta(days=1)).day)
    append(r, qs, _("Tomorrow's birthdays"),  "birth")
    
    qs=Person.objects.filter(birth__month=(date.today()+timedelta(days=2)).month, birth__day=(date.today()+timedelta(days=2)).day)
    append(r, qs, _("Day after Tomorrow's birthdays"),  "birth")
    
    for i in range(3, 31):
        qs=Person.objects.filter(birth__month=(date.today()+timedelta(days=i)).month, birth__day=(date.today()+timedelta(days=i)).day)
        append(r, qs, _("Next 30 day's birthdays"),  "birth")
        
    
    
    qs=Person.objects.filter(death__month=date.today().month, death__day=date.today().day)
    append(r, qs, _("Death"),  "death")

    
    return Response(r, status.HTTP_200_OK)
