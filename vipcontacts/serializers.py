from vipcontacts.models import Alias, Person, Address, Group, RelationShip, Job, Log, Phone, Mail, Search,  Blob
from rest_framework import serializers
from base64 import b64decode

class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('url', 'id', 'retypes',  'address', 'city',  'code',  'country',   'dt_update',  'dt_obsolete', 'person')

class AliasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alias
        fields = ('id','url', 'name',  'dt_update',  'dt_obsolete', 'person')

        
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id','url', 'name',  'dt_update',  'dt_obsolete', 'person')
        
class MailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mail
        fields = ('id','mail',  'dt_update',  'dt_obsolete', 'retypes','person', 'url')

class PhoneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Phone
        fields = ('id','url', 'phone',  'dt_update',  'dt_obsolete', 'retypes','person')

class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = ('id','url', 'dt_update', 'dt_obsolete', 'organization', 'profession', 'title', 'department', 'person')

class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = ('url',  'id', 'datetime','retypes',  'text',   'person')

class RelationShipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RelationShip
        fields = ('id','url',  'dt_update',  'dt_obsolete',  'person','retypes', 'destiny')
    
class SearchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Search
        fields = ('id','url',  'string',  'chips','person')
        
class BlobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Blob
        fields = ('id','url',  'dt_update','dt_obsolete', 'blob',  'mime', 'name', 'photocontact','person')
        
    def create(self, validated_data):
        request = self.context.get("request")
        ## Converts base 64 string to  bytes
        validated_data['blob']=b64decode(request.data['blob'].encode('utf-8'))
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        return created
    
    ## Update doesn't update blob, only changes metadata
    def update(self, instance, validated_data):
        validated_data['blob']=instance.blob
        updated=serializers.HyperlinkedModelSerializer.update(self, instance, validated_data)
        return updated
    
class PersonSerializer(serializers.HyperlinkedModelSerializer):
    relationship = RelationShipSerializer( many=True, read_only=True)
    log=LogSerializer(many=True, read_only=True)
    alias = AliasSerializer(many=True, read_only=True)
    address = AddressSerializer(many=True,  read_only=True)
    mail = MailSerializer(many=True,  read_only=True)
    phone = PhoneSerializer(many=True,  read_only=True)
    search = SearchSerializer(many=True,  read_only=True)
    job = JobSerializer(many=True,  read_only=True)
    group = GroupSerializer(many=True,  read_only=True)
    blob=BlobSerializer(many=True, read_only=True)
    fullname = serializers.SerializerMethodField()
    
    class Meta:
        model = Person
        fields = ('dt_update','dt_obsolete','id','url', 'name', 'surname', 'surname2',  'birth', 'death', 'gender', 
        'log', 'alias', 'address', 'relationship', 'phone', 'mail', 'search', 'job', 'group', 'blob', 'fullname')
        
    def get_fullname(self, o):
        return o.fullName()
        
class PersonSerializerSearch(serializers.HyperlinkedModelSerializer):
    search = SearchSerializer(many=True,  read_only=True)
    class Meta:
        model = Person
        fields = ('id','url', 'name', 'surname', 'surname2',  'birth', 'death',  'gender',  'search')
        
        
        

