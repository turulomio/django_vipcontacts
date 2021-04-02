from vipcontacts.models import Alias, Person, Address, RelationShip, Log, Phone, Mail
from rest_framework import serializers

class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'retypes',  'address', 'city',  'code',  'country',   'dt_update',  'dt_obsolete', 'person')

class AliasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alias
        fields = ('id', 'name',  'dt_update',  'dt_obsolete', 'person')
        
class MailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mail
        fields = ('id', 'mail',  'dt_update',  'dt_obsolete', 'retypes','person')

class PhoneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Phone
        fields = ('id', 'phone',  'dt_update',  'dt_obsolete', 'retypes','person')

class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = ('id', 'datetime','retypes',  'text',   'person')


class RelationShipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RelationShip
        fields = ('id',  'dt_update',  'dt_obsolete','retypes', 'destiny',  'person',)

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    relationship = RelationShipSerializer( many=True, read_only=True)
    logs=LogSerializer(many=True, read_only=True)
    alias = AliasSerializer(many=True, read_only=True)
    address = AddressSerializer(many=True,  read_only=True)
    mail = MailSerializer(many=True,  read_only=True)
    phone = PhoneSerializer(many=True,  read_only=True)
    
    class Meta:
        model = Person
        fields = ('id', 'name', 'surname', 'surname2',  'birth', 'death', 'gender', 
        'logs', 'alias', 'address', 'relationship', 'phone', 'mail')
