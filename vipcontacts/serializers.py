from vipcontacts.models import Person
from rest_framework import serializers


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name', 'surname', 'surname2',  'birth', 'death', 'gender')


