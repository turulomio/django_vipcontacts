from datetime import date
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _ #With gettext it doesn't work onky with gettext_lazy. Reason?
from pycountry import countries

#Create countries class
LIST_COUNTRIES=[]
for  country in countries:
    LIST_COUNTRIES.append((country.alpha_2, country.name))
    
    
def get_country_name(code):
    return countries.get(alpha_2=code).name

def create_log(object,  fields, dt_update=None, person=None):
    dt_update=object.dt_update if dt_update is None else dt_update
    person=object.person if person is None else person
    r=[]
    for field in fields:
        r.append((field,  getattr(object, field)))
    s=f"{object.__class__.__name__}, {r}"
    l=Log(datetime=dt_update, person=person, retypes=LogType.ContactValueAdded, text=s)
    l.save()    
    
    
def delete_log(object,  fields, dt_update=None, person=None):
    person=object.person if person is None else person
    r=[]
    for field in fields:
        r.append((field,  getattr(object, field)))
    s=f"{object.__class__.__name__}, {r}"
    l=Log(datetime=timezone.now(), person=person, retypes=LogType.ContactValueDeleted, text=s)
    l.save()    
    
def update_log( old, new_validated_data, fields, dt_update=None, person=None):
    dt_update=new_validated_data['dt_update'] if dt_update is None else dt_update
    person=new_validated_data['person'] if person is None else person
    r=[]
    for field in fields:
        old_field= getattr(old, field)
        new_field=new_validated_data[field]
        if old_field!=new_field:
            r.append((field,  old_field, new_field))
    s=f"{old.__class__.__name__}, {old.id}, {r}"
    l=Log(datetime=dt_update, person=person, retypes=LogType.ContactValueChanged, text=s)
    l.save()


class PersonGender(models.IntegerChoices):
    Man = 0, _('Man')
    Woman = 1, _('Woman')

    @classmethod
    def get_label(cls, n):
        for id, name in PersonGender.choices:
            if id==n:
                return name
        return None

# Create your models here.
class Person(models.Model):
    dt_update=models.DateTimeField(blank=False, null=False, default=timezone.now)
    dt_obsolete=models.DateTimeField(blank=False, null=True)
    name = models.CharField(max_length=100, blank=True, null=False)
    surname = models.CharField(max_length=100, blank=True, null=False)
    surname2 = models.CharField(max_length=100, blank=True, null=False)
    birth=models.DateField(blank=False, null=True)
    death=models.DateField(blank=False, null=True)
    gender=models.IntegerField(choices=PersonGender.choices, blank=False,  null=False)

    class Meta:
        managed = True
        db_table = 'persons'
        
    @staticmethod
    def post_payload(name="Turulomio", surname="García",  surname2="Pérez", birth=date.today(), death=None, gender=1):
        return {
            "name":  name,
            "surname":surname, 
            "surname2":surname2, 
            "birth":birth, 
            "death":death, 
            "gender":gender, 
          
        }
        
        
    @transaction.atomic
    def save(self, *args, **kwargs):
        self.dt_update=timezone.now()
        super().save(*args, **kwargs)

    def fullName(self):
        return f"{str(self.name)} {str(self.surname)} {str(self.surname2)}"
        
    def __str__(self):
        return f"Person: {self.fullName()} ({str(self.birth)}) #{str(self.id)}"
    def create_log( self, new):
        create_log(new, ['name', 'surname', 'surname2', 'birth', 'death', 'gender'], person=self)

    def update_log( self, old, new_validated_data):
        update_log(old, new_validated_data, ['dt_update', 'dt_obsolete', 'name', 'surname', 'surname2', 'birth', 'death', 'gender'], person=self)

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
        
        ## SEARCH STRINGS
        s=x["name"]
        s=s+add(x["surname"])
        s=s+add(x["surname2"])
        s=s+add(x["birth"])
        s=s+add(x["death"])
        for o in x["mail"]:
            s=s+add(o["mail"])
        for o in x["phone"]:
            s=s+add(o["phone"]) #+34 655 65 65 65
            s=s+add(o["phone"].replace(" ", "")) #+346556565
        for o in x["address"]:
            s=s+add(o["address"])
            s=s+add(o["city"])
        for o in x["log"]:
            if o["retypes"]==LogType.Personal:
                s=s+add(o["text"])
        for o in x["alias"]:
            s=s+add(o["name"])
        for o in x["job"]:
            s=s+add(o["profession"])
            s=s+add(o["organization"])
            s=s+add(o["department"])
            s=s+add(o["title"])
#        for o in x["relationship"]:
#            destiny=person_from_person_url(o["destiny"])
#            s=s+add(destiny.fullName())
            
        ## CHIPS
        chips=set()
        for o in x['group']:
            if o["dt_obsolete"] is None:
                chips.add(o["name"])
        
        lengthjobs=len(x['job'])
        if lengthjobs>0:
            lastjob=x['job'][lengthjobs-1]
            if len(lastjob["profession"])>0:
                chips.add(lastjob["profession"])
            if len(lastjob["organization"])>0:
                chips.add(lastjob["organization"])
            if len(lastjob["department"])>0:
                chips.add(lastjob["department"])
            if len(lastjob["title"])>0:
                chips.add(lastjob["title"])

        ## SAVE OBJECT
        Search.objects.filter(person=self).delete()
        search=Search( person=self, string=s,  chips=list(chips))
        search.save()
        
class LogType(models.IntegerChoices):
    ContactValueChanged= 0, _('Contact data changed')
    ContactValueAdded = 1, _('Contact data added')
    ContactValueDeleted = 2, _('Contact data deleted')
    ContactMerge = 3, _('Contact merge')
    
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
        
    def __str__(self):
        return f"Log: {self.text} #{self.id}"
    
    @staticmethod
    def post_payload(person, datetime_=timezone.now(),  retypes=1, text="This is a log"):
        return {
            "person":  person,
            "datetime":datetime_,
            "retypes":retypes, 
            "text":text, 
        }
        
class Alias(models.Model):
    person = models.ForeignKey('Person', related_name="alias",  on_delete=models.CASCADE, blank=False, null=False)
    dt_update=models.DateTimeField(blank=False, null=False, default=timezone.now)
    dt_obsolete=models.DateTimeField(blank=False, null=True)
    name=models.CharField(max_length=100, blank=False, null=False)
    class Meta:
        managed = True
        db_table = 'alias'
    @transaction.atomic
    def save(self, *args, **kwargs):
        self.person.dt_update=timezone.now()
        self.person.save()
        self.dt_update=self.person.dt_update
        super().save(*args, **kwargs)

    @staticmethod
    def post_payload(person, name="Alias for person"):
        return {
            "person":  person,
            "name":name, 
        }
        

    def create_log( self, new):
        create_log(new, ['name', ])

    def update_log( self, old, new_validated_data):
        update_log(old, new_validated_data, ['dt_update', 'dt_obsolete', 'name', ])

    def delete_log( self):
        delete_log(self, ['dt_update', 'dt_obsolete', 'name', ])
        
        
    
class Group(models.Model):
    person = models.ForeignKey('Person', related_name="group",  on_delete=models.CASCADE, blank=False, null=False)
    dt_update=models.DateTimeField(blank=False, null=False, default=timezone.now)
    dt_obsolete=models.DateTimeField(blank=False, null=True)
    name=models.CharField(max_length=100, blank=False, null=False)
    class Meta:
        managed = True
        db_table = 'groups'
        
    @transaction.atomic
    def save(self, *args, **kwargs):
        self.person.dt_update=timezone.now()
        self.person.save()
        self.dt_update=self.person.dt_update
        super().save(*args, **kwargs)

    @staticmethod
    def post_payload(person, name="Group for person"):
        return {
            "person":  person,
            "name":name, 
        }
    def create_log( self, new):
        create_log(new, ['name', ])

    def update_log( self, old, new_validated_data):
        update_log(old, new_validated_data, ['dt_update', 'dt_obsolete', 'name', ])
    def delete_log( self):
        delete_log(self, ['dt_update', 'dt_obsolete', 'name', ])

    def __str__(self):
        return f"Group: {self.name} #{self.id}"

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
    Friend= 10,  _('Friend')
    Boss= 11,  _('Boss')
    Subordinate= 12,  _('Subordinate')
    Cousin=13,  _('Cousin')
    Brother=14,  _('Brother')
    Sister=15,  _('Sister')
    Couple=16,  _('Couple')
    MotherInLaw=17,  _('Mother in law')
    FatherInLaw=18,   _('Father in law')
    DaughterInLaw=19,   _('Daughter in law')
    SonInLaw=20,   _('Son in law')
    ExCouple=21,  _('Ex couple')
    Nephew=22,  _("Nephew")
    Niece=23,  _("Niece")
    Stepfather=24,  _("Stepfather")
    Stepmother=25,  _("Stepmother")
    Stepbrother=26,  _("Stepbrother")
    Stepsister=27,  _("Stepsister")
    Uncle=28,  _("Uncle")
    Aunt=29,  _("Aunt")
    Secretary=30,  _("Secretary")

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
        
    @transaction.atomic
    def save(self, *args, **kwargs):
        self.person.dt_update=timezone.now()
        self.person.save()
        self.dt_update=self.person.dt_update
        super().save(*args, **kwargs)

    def create_log( self, new):
        create_log(new, ['retypes', 'destiny' ])

    def update_log( self, old, new_validated_data):
        update_log(old, new_validated_data, ['dt_update', 'dt_obsolete', 'retypes', 'destiny' ])

    def delete_log( self):
        delete_log(self, ['dt_update', 'dt_obsolete', 'retypes', 'destiny' ])

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
    code=models.CharField(max_length=10, blank=True, null=True)
    city=models.CharField(max_length=100, blank=False, null=False)
    country=models.CharField(max_length=2, choices=LIST_COUNTRIES,  blank=False, null=False)    
    class Meta:
        managed = True
        db_table = 'addresses'

    def __str__(self):
        return f"Address: {self.address}, {self.code} {self.city}, {self.country} #{self.id}"
        
    @transaction.atomic
    def save(self, *args, **kwargs):
        self.person.dt_update=timezone.now()
        self.person.save()
        self.dt_update=self.person.dt_update
        super().save(*args, **kwargs)

    def create_log( self, new):
        create_log(new, ['retypes', 'address', 'code', 'city', 'country'])

    def update_log( self, old, new_validated_data):
        update_log(old, new_validated_data, ['dt_update', 'dt_obsolete', 'retypes', 'address', 'code', 'city', 'country'])

    def delete_log( self):
        delete_log(self, ['dt_update', 'dt_obsolete', 'retypes', 'address', 'code', 'city', 'country'])
            
    @staticmethod
    def post_payload(person, retypes=1, address="Home", code="28001",  city="Home town",  country="ES"):
        return {
            "person":  person,
            "retypes":retypes, 
            "address":address, 
            "code":code, 
            "city":city, 
            "country":country, 
          
        }
        
    
class Job(models.Model):
    person = models.ForeignKey('Person',related_name="job",  on_delete= models.CASCADE, blank=False, null=False)
    dt_update=models.DateTimeField(blank=False, null=False, default=timezone.now)
    dt_obsolete=models.DateTimeField(blank=False, null=True)
    organization=models.CharField(max_length=300, blank=True, null=False)
    profession=models.CharField(max_length=300, blank=True, null=False)
    title=models.CharField(max_length=300, blank=True, null=False)
    department=models.CharField(max_length=300, blank=True, null=False)
    class Meta:
        managed = True
        db_table = 'jobs'
        

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.person.dt_update=timezone.now()
        self.person.save()
        self.dt_update=self.person.dt_update
        super().save(*args, **kwargs)
        
    @staticmethod
    def post_payload(person, organization="Person organization", profession="Person profession",  title="Person title",  department="Person department"):
        return {
            "person":  person,
            "organization":organization, 
            "profession":profession, 
            "title":title, 
            "department":department, 
        }
        
    def create_log( self, new):
        create_log(new, ['organization', 'profession', 'title', 'department'])

    def update_log( self, old, new_validated_data):
        update_log(old, new_validated_data, ['dt_update', 'dt_obsolete', 'organization', 'profession', 'title', 'department'])

    def __str__(self):
        return f"Job: {self.organization}"


    def delete_log( self):
        delete_log(self, ['dt_update', 'dt_obsolete', 'organization', 'profession', 'title', 'department'])

class PhoneType(models.IntegerChoices):
    Home = 0, _('Home')     
    Work= 1, _('Work')
    PersonalMobile= 3, _('Personal mobile')
    WorkMobile= 4, _('Work mobile')
    Others= 5, _('Others')
    FaxWork=6,  _('Work fax')
    WorkInternalPhone=7,  _('Work internal phone')
    WorkInternalMobile=8,  _('Work internal mobile')
    
class Phone(models.Model):
    person = models.ForeignKey('Person', related_name="phone",  on_delete= models.CASCADE, blank=False, null=False)
    dt_update=models.DateTimeField(blank=False, null=False, default=timezone.now)
    dt_obsolete=models.DateTimeField(blank=False, null=True)
    retypes=models.IntegerField(choices=PhoneType.choices, blank=False,  null=False)
    phone=models.CharField(max_length=50, blank=False, null=True) 
    class Meta:
        managed = True
        db_table = 'phones'

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.person.dt_update=timezone.now()
        self.person.save()
        self.dt_update=self.person.dt_update
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Phone: {self.phone} #{self.id}"

    def create_log( self, new):
        create_log(new, ['retypes', 'phone' ])

    def update_log( self, old, new_validated_data):
        update_log(old, new_validated_data, ['dt_update', 'dt_obsolete', 'retypes', 'phone' ])
        
    def delete_log( self):
        delete_log(self, ['dt_update', 'dt_obsolete', 'retypes', 'phone' ])
        
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


    @transaction.atomic
    def save(self, *args, **kwargs):
        self.person.dt_update=timezone.now()
        self.person.save()
        self.dt_update=self.person.dt_update
        super().save(*args, **kwargs)

    def create_log( self, new):
        create_log(new, ['retypes', 'mail' ])

    def update_log( self, old, new_validated_data):
        update_log(old, new_validated_data, ['dt_update', 'dt_obsolete', 'retypes', 'mail' ])
    def __str__(self):
        return f"Mail: {self.mail} of type {self.retypes}"

    def delete_log( self):
        delete_log(self, ['dt_update', 'dt_obsolete', 'retypes', 'mail' ])

class Search(models.Model):
    person = models.ForeignKey('Person', related_name="search",  on_delete= models.CASCADE, blank=False, null=False)
    string = models.TextField(blank=True, null=False)
    chips=models.TextField(blank=True,  null=True)
    class Meta:
        managed = True
        db_table = 'searchs'
        
    def __str__(self):
        return f"Searchs: {self.string}"
        
class BlobMimeType(models.TextChoices):
    png="image/png", "image/png"
    jpeg="image/jpeg", "image/jpeg"
    text="text/plain", "text/plain"
        
class Blob(models.Model):
    dt_update=models.DateTimeField(blank=False, null=False, default=timezone.now)
    dt_obsolete=models.DateTimeField(blank=False, null=True)
    person = models.ForeignKey('Person', related_name="blob",  on_delete= models.CASCADE, blank=False, null=False)
    blob=models.BinaryField(null=False)
    mime=models.CharField(choices=BlobMimeType.choices, max_length=100, blank=False, null=False)
    name=models.CharField(max_length=100, blank=False, null=False)
    photocontact=models.BooleanField(max_length=100, null=False,  default=False)
    class Meta:
        managed = True
        db_table = 'blobs'
        
    @transaction.atomic
    def save(self, *args, **kwargs):
        self.person.dt_update=timezone.now()
        self.person.save()
        self.dt_update=self.person.dt_update
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Blob: {self.name}.{self.extension()}"

    def extension(self):
        if self.mime==BlobMimeType.png:
            return "png"
        elif self.mime==BlobMimeType.jpeg:
            return "jpg"

def person_from_person_url(s):
    arr=s.split("/")
    id=arr[len(arr)-2]
    return Person.objects.get(pk=id)
