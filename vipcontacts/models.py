from django.db import models
from django.utils.translation import gettext as _

class PersonGender(models.IntegerChoices):
    Man = 0, _('Man')
    Woman = 1, _('Woman')

class PersonRelationType(models.IntegerChoices):
    Wife = 0, _('Wife')
    Husband= 1, _('Husband')
    Son = 2, _('Son')
    Daughter= 3, _('Daughter')

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

class PersonRelation(models.Model):
    dt_update=models.DateTimeField(blank=False, null=False)
    dt_obsolete=models.DateTimeField(blank=False, null=True)
    person = models.ForeignKey('Person', models.DO_NOTHING, blank=False, null=False, related_name="person")
    type=models.IntegerField(choices=PersonRelationType.choices, blank=False,  null=False)
    relationated=models.ForeignKey('Person', models.DO_NOTHING, blank=False, null=False, related_name="relationated")
    class Meta:
        managed = False
        db_table = 'personsrelations'

class Address(models.Model):
    person = models.ForeignKey('Person', models.DO_NOTHING, blank=False, null=False)
    dt_update=models.DateTimeField(blank=False, null=False)
    dt_obsolete=models.DateTimeField(blank=False, null=True)
    address=models.CharField(max_length=300, blank=False, null=False)
    code=models.CharField(max_length=10, blank=False, null=True)
    city=models.CharField(max_length=100, blank=False, null=False)
    countrys=models.CharField(max_length=100, blank=False, null=False)    
    class Meta:
        managed = False
        db_table = 'adresses'
    
class Log(models.Model):
    person = models.ForeignKey('Person', models.DO_NOTHING, blank=False, null=False)
    dt_update=models.DateTimeField(blank=False, null=False)
    model=models.CharField(max_length=30, blank=False, null=False)
    before=models.CharField(max_length=1000, blank=False, null=False)
    after=models.CharField(max_length=1000, blank=False, null=False)
    class Meta:
        managed = False
        db_table = 'logs'
