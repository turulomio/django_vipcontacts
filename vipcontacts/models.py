from datetime import date
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _ #With gettext it doesn't work onky with gettext_lazy. Reason?
from pycountry import countries
from pydicts import casts, lod
from simple_history.models import HistoricalRecords

#Create countries class
LIST_COUNTRIES=[]
for  country in countries:
    LIST_COUNTRIES.append((country.alpha_2, country.name))
    
    
def get_country_name(code):
    return countries.get(alpha_2=code).name

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

    history= HistoricalRecords()
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
        self.update_search_string()

    def fullName(self):
        return f"{str(self.name)} {str(self.surname)} {str(self.surname2)}"
        
    def __str__(self):
        return f"Person: {self.fullName()} ({str(self.birth)}) #{str(self.id)}"

    ## Generate a search string
    def update_search_string( self):
        def add(s):
            if s==None:
                return ""
            else:
                return " " + str(s)
        ######
        if self.id is None:
            raise Exception("You must save person before update_search_string")

        ## SEARCH STRINGS
        s=""
        s=s + add(self.name)
        s=s+add(self.surname)
        s=s+add(self.surname2)
        s=s+add(self.birth)
        s=s+add(self.death)
        for mail in self.mail.filter(dt_obsolete__isnull=True):
            s=s+add(mail.mail)
        for phone in self.phone.filter(dt_obsolete__isnull=True):
            s=s+add(phone.phone) #+34 655 65 65 65
            s=s+add(phone.phone.replace(" ", "")) #+346556565
        for address in self.address.filter(dt_obsolete__isnull=True):
            s=s+add(address.address)
            s=s+add(address.address)
        for log in self.log.filter(retypes__gte=100):
            if log.retypes==LogType.Personal:
                s=s+add(log.text)
        for alias in self.alias.filter(dt_obsolete__isnull=True):
            s=s+add(alias.name)
        for job in self.job.filter(dt_obsolete__isnull=True):
            s=s+add(job.profession)
            s=s+add(job.organization)
            s=s+add(job.department)
            s=s+add(job.title)
#        for o in x["relationship"]:
#            destiny=person_from_person_url(o["destiny"])
#            s=s+add(destiny.fullName())
            
        ## CHIPS
        chips=set()
        for group in self.group.filter(dt_obsolete__isnull=True):
                chips.add(group.name)
        
        for job in self.job.filter(dt_obsolete__isnull=True):
            if not casts.is_noe(job.profession):
                chips.add(job.profession)
            if not casts.is_noe(job.organization):
                chips.add(job.organization)
            if not casts.is_noe(job.department):
                chips.add(job.department)
            if not casts.is_noe(job.title):
                chips.add(job.title)


        ## SAVE OBJECT
        Search.objects.filter(person=self).delete()
        search=Search( person=self, string=s,  chips=list(chips))
        search.save()
        
    @staticmethod
    def historical_register(id, console=False):
        """
            Return a list of dictionaries with all person changes
            
            Id is used due to person can be deleted, but id will remain in historic tables
        """
        def diff_dictionaries(old, new):   
            r=[]
            if old is None:
                for field in new._meta.fields:
                    if field.name in ["history_id", "history_date", "history_change_reason", "history_type", "history_user"]:
                        continue
                    d={}
                    d["datetime"]=new.history_date
                    d["model"]=new.__class__.__name__
                    d["id"]=new.id
                    d["field"]=field.name
                    d["old"]=None
                    d["new"]=str(getattr(new, field.name))
                    d["user"]=str(new.history_user)
                    d["type"]="+"
                    r.append(d)
            else:
                delta=new.diff_against(old)
                for change in delta.changes:
                    d={}
                    d["datetime"]=new.history_date
                    d["model"]=new.__class__.__name__
                    d["id"]=new.id
                    d["field"]=change.field
                    d["old"]=str(change.old)
                    d["new"]=str(change.new)
                    d["user"]=str(new.history_user)
                    d["type"]=new.history_type
                    r.append(d)
            return r
        #############################################        
        r={"diff": []}
        #Person
        histories_person=Person.history.filter(id=id).order_by("history_date")
        r["person"]=list(histories_person.values())
        for i in range(len(r["person"])):
            r["diff"]+=diff_dictionaries(None if i==0 else histories_person[i-1], histories_person[i])
            
        #Alias
        histories_alias=Alias.history.filter(person__id=id).order_by("history_date")
        r["alias"]=list(histories_alias.values())
        for i in range(len(histories_alias)):
            r["diff"]+=diff_dictionaries(None if i==0 else histories_alias[i-1], histories_alias[i])
            
        #Group
        histories_group=Group.history.filter(person__id=id).order_by("history_date")
        r["group"]=list(histories_group.values())
        for i in range(len(histories_group)):
            r["diff"]+=diff_dictionaries(None if i==0 else histories_group[i-1], histories_group[i])

        #Address
        histories_address=Address.history.filter(person__id=id).order_by("history_date")
        r["address"]=list(histories_address.values())
        for i in range(len(histories_address)):
            r["diff"]+=diff_dictionaries(None if i==0 else histories_address[i-1], histories_address[i])
                
        #Mail
        histories_mail=Mail.history.filter(person__id=id).order_by("history_date")
        r["mail"]=list(histories_mail.values())
        for i in range(len(histories_mail)):
            r["diff"]+=diff_dictionaries(None if i==0 else histories_mail[i-1], histories_mail[i])
            
        #Phone
        histories_phone=Phone.history.filter(person__id=id).order_by("history_date")
        r["phone"]=list(histories_phone.values())
        for i in range(len(histories_phone)):
            r["diff"]+=diff_dictionaries(None if i==0 else histories_phone[i-1], histories_phone[i])
            
        #RelationShip
        histories_relationship=RelationShip.history.filter(person__id=id).order_by("history_date")
        r["relationship"]=list(histories_relationship.values())
        for i in range(len(histories_relationship)):
            r["diff"]+=diff_dictionaries(None if i==0 else histories_relationship[i-1], histories_relationship[i])

        #Job
        histories_job=Job.history.filter(person__id=id).order_by("history_date")
        r["job"]=list(histories_job.values())
        for i in range(len(histories_job)):
            r["diff"]+=diff_dictionaries(None if i==0 else histories_job[i-1], histories_job[i])
                
        #Log
        histories_log=Log.history.filter(person__id=id).order_by("history_date")
        r["log"]=list(histories_log.values())
        for i in range(len(histories_log)):
            r["diff"]+=diff_dictionaries(None if i==0 else histories_log[i-1], histories_log[i])

        #Diff
        if console:
            print("PERSON")
            lod.lod_print(r["person"])
            print("ALIAS")
            lod.lod_print(r["alias"])
            print("ADDRESS")
            lod.lod_print(r["address"])
            print("MAIL")
            lod.lod_print(r["mail"])
            print("PHONE")
            lod.lod_print(r["phone"])
            print("RELATIONSHIP")
            lod.lod_print(r["relationship"])
            print("GROUP")
            lod.lod_print(r["group"])
            print("JOB")
            lod.lod_print(r["job"])
            print("LOG")
            lod.lod_print(r["log"])
            print("DIFF")
            lod.lod_print(r["diff"])
        return r
            
        
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
    
    history= HistoricalRecords()
    
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
        
        
    @transaction.atomic
    def save(self, *args, **kwargs):
        self.dt_update=timezone.now()
        super().save(*args, **kwargs)
        self.person.dt_update=self.datetime
        self.person.save() #Has implicit update_search string
        
class Alias(models.Model):
    person = models.ForeignKey('Person', related_name="alias",  on_delete=models.CASCADE, blank=False, null=False)
    dt_update=models.DateTimeField(blank=False, null=False, default=timezone.now)
    dt_obsolete=models.DateTimeField(blank=False, null=True)
    name=models.CharField(max_length=100, blank=False, null=False)
    
    history= HistoricalRecords()
    class Meta:
        managed = True
        db_table = 'alias'
    @transaction.atomic
    def save(self, *args, **kwargs):
        self.dt_update=timezone.now()
        super().save(*args, **kwargs)
        self.person.dt_update=self.dt_update
        self.person.save() #Has implicit update_search string
        
    @staticmethod
    def post_payload(person, name="Alias for person"):
        return {
            "person":  person,
            "name":name, 
        }
        
    
class Group(models.Model):
    person = models.ForeignKey('Person', related_name="group",  on_delete=models.CASCADE, blank=False, null=False)
    dt_update=models.DateTimeField(blank=False, null=False, default=timezone.now)
    dt_obsolete=models.DateTimeField(blank=False, null=True)
    name=models.CharField(max_length=100, blank=False, null=False)
    
    history= HistoricalRecords()
    class Meta:
        managed = True
        db_table = 'groups'
        
    @transaction.atomic
    def save(self, *args, **kwargs):
        self.dt_update=timezone.now()
        super().save(*args, **kwargs)
        self.person.dt_update=self.dt_update
        self.person.save() #Has implicit update_search string

    @staticmethod
    def post_payload(person, name="Group for person"):
        return {
            "person":  person,
            "name":name, 
        }

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
    
    history= HistoricalRecords()
    class Meta:
        managed = True
        db_table = 'relationship'
        
    @transaction.atomic
    def save(self, *args, **kwargs):
        self.dt_update=timezone.now()
        super().save(*args, **kwargs)
        self.person.dt_update=self.dt_update
        self.person.save() #Has implicit update_search string


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
    
    history= HistoricalRecords()
    
    class Meta:
        managed = True
        db_table = 'addresses'

    def __str__(self):
        return f"Address: {self.address}, {self.code} {self.city}, {self.country} #{self.id}"
        
    @transaction.atomic
    def save(self, *args, **kwargs):
        self.dt_update=timezone.now()
        super().save(*args, **kwargs)
        self.person.dt_update=self.dt_update
        self.person.save() #Has implicit update_search string

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
    
    history= HistoricalRecords()
    class Meta:
        managed = True
        db_table = 'jobs'
        

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.dt_update=timezone.now()
        super().save(*args, **kwargs)
        self.person.dt_update=self.dt_update
        self.person.save() #Has implicit update_search string
        
    @staticmethod
    def post_payload(person, organization="Person organization", profession="Person profession",  title="Person title",  department="Person department"):
        return {
            "person":  person,
            "organization":organization, 
            "profession":profession, 
            "title":title, 
            "department":department, 
        }
 
    def __str__(self):
        return f"Job: {self.organization}"

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
    
    history= HistoricalRecords()
    class Meta:
        managed = True
        db_table = 'phones'

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.dt_update=timezone.now()
        super().save(*args, **kwargs)
        self.person.dt_update=self.dt_update
        self.person.save() #Has implicit update_search string

    def __str__(self):
        return f"Phone: {self.phone} #{self.id}"

        
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
    
    history= HistoricalRecords()
    class Meta:
        managed = True
        db_table = 'mails'


    @transaction.atomic
    def save(self, *args, **kwargs):
        self.dt_update=timezone.now()
        super().save(*args, **kwargs)
        self.person.dt_update=self.dt_update
        self.person.save() #Has implicit update_search string

    def __str__(self):
        return f"Mail: {self.mail} of type {self.retypes}"



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
