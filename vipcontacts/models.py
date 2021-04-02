from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
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
        
    def __str__(self):
        return f"{str(self.name)} {str(self.surname)} {str(self.surname2)}"
class LogType(models.IntegerChoices):
    ContactValueChanged= 0, _('Contact value changed')
    ContactValueAdded = 1, _('Contact value added')
    Personal=2, _("Personal")

class Log(models.Model):
    person = models.ForeignKey('Person', related_name="logs", on_delete= models.CASCADE, blank=False, null=False)
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

class PersonRelationType(models.IntegerChoices):
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
    person = models.ForeignKey('Person', related_name="origin", on_delete=models.CASCADE, blank=False, null=False,)
    retypes=models.IntegerField(choices=PersonRelationType.choices, blank=False,  null=False)
    destiny =  models.ForeignKey('Person', related_name="+", on_delete=models.DO_NOTHING, blank=False, null=False)
    class Meta:
        managed = True
        db_table = 'relationship'


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
        db_table = 'adresses'


class PhoneType(models.IntegerChoices):
    Home = 0, _('Home')
    Work= 1, _('Work')
    PersonalMobile= 3, _('Home mobile')
    WorkMobile= 4, _('Personal mobile')
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
        
        
class MailType(models.IntegerChoices):
    Home = 0, _('Personal')
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

