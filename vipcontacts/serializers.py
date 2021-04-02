from vipcontacts.models import Alias, Person, Address, RelationShip
from rest_framework import serializers

class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'type',  'address', 'city',  'code',  'country',   'dt_update',  'dt_obsolete', 'person')


class AliasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alias
        fields = ('id', 'name',  'dt_update',  'dt_obsolete', 'person')


class RelationShipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RelationShip
        fields = ('id',  'dt_update',  'dt_obsolete', 'person','type', 'destiny')


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    relationship = RelationShipSerializer(many=True, read_only=True)
    alias = AliasSerializer(many=True, read_only=True)
    address = AddressSerializer(many=True,  read_only=True)
    class Meta:
        model = Person
        fields = ('id', 'name', 'surname', 'surname2',  'birth', 'death', 'gender', 'alias', 'address', 'relationship')
