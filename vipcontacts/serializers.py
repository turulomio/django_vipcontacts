from vipcontacts.models import Alias, Person, Address
from rest_framework import serializers

class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
#        fields = ('id', 'name',  'dt_update',  'dt_obsolete', 'person')
        fields = '__all__'

class AliasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alias
        fields = ('id', 'name',  'dt_update',  'dt_obsolete')
        fields = '__all__'

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    alias = AliasSerializer(many=True, read_only=True)
    address = AddressSerializer(many=True,  read_only=True)
    class Meta:
        model = Person
        fields = ('id', 'name', 'surname', 'surname2',  'birth', 'death', 'gender', 'alias', 'address')




        
