from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _ #With gettext it doesn't work onky with gettext_lazy. Reason?
from pycountry import countries

#Create countries class
LIST_COUNTRIES=[]
for  country in countries:
    LIST_COUNTRIES.append((country.alpha_2, country.name))



class PersonGender(models.IntegerChoices):
    Man = 0, _('Man')
    Woman = 1, _('Woman')

    

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=100, blank=True, null=False)
    surname = models.CharField(max_length=100, blank=True, null=False)
    surname2 = models.CharField(max_length=100, blank=True, null=False)
    birth=models.DateField(blank=False, null=True)
    death=models.DateField(blank=False, null=True)
    gender=models.IntegerField(choices=PersonGender.choices, blank=False,  null=False)

    class Meta:
        managed = True
        db_table = 'persons'
        
    def fullName(self):
        return f"{str(self.name)} {str(self.surname)} {str(self.surname2)}"
        
    def __str__(self):
        return f"Person: {self.fullName()} ({str(self.birth)}) #{str(self.id)}"
    def create_log( self, new):
        create_log(new, ['name', 'surname', 'surname2', 'birth', 'death', 'gender'])

    def update_log( self, old, new_validated_data):
        update_log(old, new_validated_data, ['dt_update', 'dt_obsolete', 'name', 'surname', 'surname2', 'birth', 'death', 'gender'])

    ## Generate a search string
    def update_search_string( self, request=None):
        def add(s):
            if s==None:
                return ""
            else:
                return " " + s
        ######
        if self.id is None:
            print("You must save person before update_search_string")
            return 
        from vipcontacts.serializers import PersonSerializer
        serializer = PersonSerializer(self, many=False,context={'request': request} )
        x=serializer.data
        s=x["name"]
        s=s+add(x["surname"])
        s=s+add(x["surname2"])
        s=s+add(x["birth"])
        s=s+add(x["death"])
        for o in x["mail"]:
            s=s+add(o["mail"])
        for o in x["phone"]:
            s=s+add(o["phone"])
        for o in x["address"]:
            s=s+add(o["address"])
            s=s+add(o["city"])
#        for o in x["log"]:
#            s=s+add(o["text"])
        for o in x["alias"]:
            s=s+add(o["name"])
#        for o in x["relationship"]:
#            s=s+add(o["name"])
        Search.objects.filter(person=self).delete()
        search=Search( person=self, string=s)
        search.save()

class LogType(models.IntegerChoices):
    ContactValueChanged= 0, _('Contact data changed')
    ContactValueAdded = 1, _('Contact data added')
    ContactValueDeleted = 2, _('Contact data deleted')
    
    #Automatic are <100
    Personal=100, _("Personal")

class Log(models.Model):
    person = models.ForeignKey('Person', related_name="log", on_delete= models.CASCADE, blank=False, null=False)
    datetime=models.DateTimeField(blank=False, null=False, default=timezone.now)
    retypes=models.IntegerField(choices=LogType.choices, blank=False,  null=False)
    text=models.TextField(blank=False, null=True)
    class Meta:
        managed = True
        db_table = 'logs'

class Alias(models.Model):
    person = models.ForeignKey('Person', related_name="alias",  on_delete=models.CASCADE, blank=False, null=False)
    dt_update=models.DateTimeField(blank=False, null=False, default=timezone.now)
    dt_obsolete=models.DateTimeField(blank=False, null=True)
    name=models.CharField(max_length=100, blank=False, null=False)
    class Meta:
        managed = True
        db_table = 'alias'
        
    def create_log( self, new):
        create_log(new, ['name', ])

    def update_log( self, old, new_validated_data):
        update_log(old, new_validated_data, ['dt_update', 'dt_obsolete', 'name', ])


class RelationShipType(models.IntegerChoices):
    Wife = 0, _('Wife')
    Husband= 1, _('Husband')
    Son = 2, _('Son')
    Daughter= 3, _('Daughter')
    Father= 4, _('Father')
    Mother= 5, _('Mother')
    Grandfather= 6, _('Grandfather')
    Grandmother= 7, _('Grandmother')
    Grandson= 8, _('Grandson')
    Granddaughter= 9, _('Granddaughter')

## person type destiny
## M Husband N
class RelationShip(models.Model):
    dt_update=models.DateTimeField(blank=False, null=False, default=timezone.now)
    dt_obsolete=models.DateTimeField(blank=False, null=True)
    person = models.ForeignKey('Person', related_name="relationship", on_delete=models.CASCADE, blank=False, null=False,)
    retypes=models.IntegerField(choices=RelationShipType.choices, blank=False,  null=False)
    destiny =  models.ForeignKey('Person', related_name="+", on_delete=models.DO_NOTHING, blank=False, null=False)
    class Meta:
        managed = True
        db_table = 'relationship'
        
    def create_log( self, new):
        create_log(new, ['retypes', 'destiny' ])

    def update_log( self, old, new_validated_data):
        update_log(old, new_validated_data, ['dt_update', 'dt_obsolete', 'retypes', 'destiny' ])

class AddressType(models.IntegerChoices):
    Home = 0, _('Home')
    Work= 1, _('Work')
    Holidays= 2, _('Vacances')
    
class Address(models.Model):
    person = models.ForeignKey('Person',related_name="address",  on_delete= models.CASCADE, blank=False, null=False)
    dt_update=models.DateTimeField(blank=False, null=False, default=timezone.now)
    dt_obsolete=models.DateTimeField(blank=False, null=True)
    retypes=models.IntegerField(choices=AddressType.choices, blank=False,  null=False)
    address=models.CharField(max_length=300, blank=False, null=False)
    code=models.CharField(max_length=10, blank=False, null=True)
    city=models.CharField(max_length=100, blank=False, null=False)
    country=models.CharField(max_length=2, choices=LIST_COUNTRIES,  blank=False, null=False)    
    class Meta:
        managed = True
        db_table = 'addresses'

    def create_log( self, new):
        create_log(new, ['retypes', 'address', 'code', 'city', 'country'])

    def update_log( self, old, new_validated_data):
        update_log(old, new_validated_data, ['dt_update', 'dt_obsolete', 'retypes', 'address', 'code', 'city', 'country'])

def create_log(object,  fields):
    r=[]
    for field in fields:
        r.append((field,  getattr(object, field)))
    s=f"{object.__class__.__name__}, {r}"
    l=Log(datetime=object.dt_update, person=object.person, retypes=LogType.ContactValueAdded, text=s)
    l.save()    
    
def update_log( old, new_validated_data, fields):
    r=[]
    for field in fields:
        old_field= getattr(old, field)
        new_field=new_validated_data[field]
        if old_field!=new_field:
            r.append((field,  old_field, new_field))
    s=f"{old.__class__.__name__}, {old.id}, {r}"
    l=Log(datetime=new_validated_data['dt_update'], person=old.person, retypes=LogType.ContactValueChanged, text=s)
    l.save()

class PhoneType(models.IntegerChoices):
    Home = 0, _('Home')     
    Work= 1, _('Work')
    PersonalMobile= 3, _('Personal mobile')
    WorkMobile= 4, _('Work mobile')
    Others= 5, _('Others')
    
class Phone(models.Model):
    person = models.ForeignKey('Person', related_name="phone",  on_delete= models.CASCADE, blank=False, null=False)
    dt_update=models.DateTimeField(blank=False, null=False, default=timezone.now)
    dt_obsolete=models.DateTimeField(blank=False, null=True)
    retypes=models.IntegerField(choices=PhoneType.choices, blank=False,  null=False)
    phone=models.CharField(max_length=20, blank=False, null=True) 
    class Meta:
        managed = True
        db_table = 'phones'

    def create_log( self, new):
        create_log(new, ['retypes', 'phone' ])

    def update_log( self, old, new_validated_data):
        update_log(old, new_validated_data, ['dt_update', 'dt_obsolete', 'retypes', 'phone' ])
        
class MailType(models.IntegerChoices):
    Personal = 0, _('Personal')
    Work= 1, _('Work')
    Other= 2, _('Other')
    
class Mail(models.Model):
    person = models.ForeignKey('Person', related_name="mail",  on_delete= models.CASCADE, blank=False, null=False)
    dt_update=models.DateTimeField(blank=False, null=False, default=timezone.now)
    dt_obsolete=models.DateTimeField(blank=False, null=True)
    retypes=models.IntegerField(choices=MailType.choices, blank=False,  null=False)
    mail=models.CharField(max_length=100, blank=False, null=True) 
    class Meta:
        managed = True
        db_table = 'mails'

    def create_log( self, new):
        create_log(new, ['retypes', 'mail' ])

    def update_log( self, old, new_validated_data):
        update_log(old, new_validated_data, ['dt_update', 'dt_obsolete', 'retypes', 'mail' ])
    def __str__(self):
        return f"Mail: {self.mail} of type {self.retypes}"

class Search(models.Model):
    person = models.ForeignKey('Person', related_name="search",  on_delete= models.CASCADE, blank=False, null=False)
    string = models.TextField(blank=True, null=False)
    class Meta:
        managed = True
        db_table = 'searchs'
        
    def __str__(self):
        return f"Searchs: {self.string}"
        
#    ## Generate a search string
#    def person_search_string(self, request=None):
#        def add(s):
#            if s==None:
#                return ""
#            else:
#                return " " + s
#        ######
#        if self.person is None:
#            print ("person_search_string set person first")
#            return ""
#        from vipcontacts.serializers import PersonSerializer
#        serializer = PersonSerializer(self.person, many=False,context={'request': request} )
#        x=serializer.data
#        s=x["name"]
#        s=s+add(x["surname"])
#        s=s+add(x["surname2"])
#        s=s+add(x["birth"])
#        s=s+add(x["death"])
#        for o in x["mail"]:
#            s=s+add(o["mail"])
#        for o in x["phone"]:
#            s=s+add(o["phone"])
#        for o in x["address"]:
#            s=s+add(o["address"])
#            s=s+add(o["city"])
#        for o in x["log"]:
#            s=s+add(o["text"])
#        for o in x["alias"]:
#            s=s+add(o["name"])
#        return s
