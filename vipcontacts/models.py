from django.db import models
from django.utils.translation import gettext as _

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
