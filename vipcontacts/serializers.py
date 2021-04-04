from vipcontacts.models import Alias, Person, Address, RelationShip, Log, Phone, Mail, Search
from rest_framework import serializers

class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('url', 'retypes',  'address', 'city',  'code',  'country',   'dt_update',  'dt_obsolete', 'person')

class AliasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alias
        fields = ('id','url', 'name',  'dt_update',  'dt_obsolete', 'person')
        
class MailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mail
        fields = ('mail',  'dt_update',  'dt_obsolete', 'retypes','person', 'url')

class PhoneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Phone
        fields = ('url', 'phone',  'dt_update',  'dt_obsolete', 'retypes','person')

class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = ('url', 'datetime','retypes',  'text',   'person')


class RelationShipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RelationShip
        fields = ('url',  'dt_update',  'dt_obsolete',  'person','retypes', 'destiny')

class SearchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Search
        fields = ('url',  'string',  'person')

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    relationship = RelationShipSerializer( many=True, read_only=True)
    log=LogSerializer(many=True, read_only=True)
    alias = AliasSerializer(many=True, read_only=True)
    address = AddressSerializer(many=True,  read_only=True)
    mail = MailSerializer(many=True,  read_only=True)
    phone = PhoneSerializer(many=True,  read_only=True)
    search = SearchSerializer(many=True,  read_only=True)
    
    def create(self, validated_data):
        p=Person.objects.create(**validated_data)
        p.update_search_string()
        return p
    
    def update(self, instance, validated_data):
        updated_person=serializers.HyperlinkedModelSerializer.update(self, instance, validated_data)
        updated_person.update_search_string()
        return updated_person
    
    class Meta:
        model = Person
        fields = ('id','url', 'name', 'surname', 'surname2',  'birth', 'death', 'gender', 
        'log', 'alias', 'address', 'relationship', 'phone', 'mail', 'search')
        
        
class PersonSerializerSearch(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('id','url', 'name', 'surname', 'surname2',  'birth')
        
        
        

