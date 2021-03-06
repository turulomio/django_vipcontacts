from vipcontacts.models import Alias, Person, Address, Group, RelationShip, Job, Log, Phone, Mail, Search,  Blob
from rest_framework import serializers

class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('url', 'retypes',  'address', 'city',  'code',  'country',   'dt_update',  'dt_obsolete', 'person')
    
    def create(self, validated_data):
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        created.person.update_search_string()
        created.create_log(created)
        return created
    
    def update(self, instance, validated_data):
        instance.update_log(instance, validated_data)
        updated=serializers.HyperlinkedModelSerializer.update(self, instance, validated_data)
        updated.person.update_search_string()
        return updated

class AliasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alias
        fields = ('id','url', 'name',  'dt_update',  'dt_obsolete', 'person')

    def create(self, validated_data):
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        created.person.update_search_string()
        created.create_log(created)
        return created
    
    def update(self, instance, validated_data):
        instance.update_log(instance, validated_data)
        updated=serializers.HyperlinkedModelSerializer.update(self, instance, validated_data)
        updated.person.update_search_string()
        return updated
        
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id','url', 'name',  'dt_update',  'dt_obsolete', 'person')

    def create(self, validated_data):
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        created.person.update_search_string()
        created.create_log(created)
        return created
    
    def update(self, instance, validated_data):
        instance.update_log(instance, validated_data)
        updated=serializers.HyperlinkedModelSerializer.update(self, instance, validated_data)
        updated.person.update_search_string()
        return updated
        
class MailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mail
        fields = ('mail',  'dt_update',  'dt_obsolete', 'retypes','person', 'url')

    def create(self, validated_data):
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        created.person.update_search_string()
        created.create_log(created)
        return created
    
    def update(self, instance, validated_data):
        instance.update_log(instance, validated_data)
        updated=serializers.HyperlinkedModelSerializer.update(self, instance, validated_data)
        updated.person.update_search_string()
        return updated

class PhoneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Phone
        fields = ('url', 'phone',  'dt_update',  'dt_obsolete', 'retypes','person')

    def create(self, validated_data):
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        created.person.update_search_string()
        created.create_log(created)
        return created
    
    def update(self, instance, validated_data):
        instance.update_log(instance, validated_data)
        updated=serializers.HyperlinkedModelSerializer.update(self, instance, validated_data)
        updated.person.update_search_string()
        return updated

class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = ('url', 'dt_update', 'dt_obsolete', 'organization', 'profession', 'title', 'department', 'person')
    
    def create(self, validated_data):
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        created.person.update_search_string()
        created.create_log(created)
        return created
    
    def update(self, instance, validated_data):
        instance.update_log(instance, validated_data)
        updated=serializers.HyperlinkedModelSerializer.update(self, instance, validated_data)
        updated.person.update_search_string()
        return updated

class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = ('url', 'datetime','retypes',  'text',   'person')

    
    def create(self, validated_data):
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        created.person.update_search_string()
        #created.create_log(created)
        return created
    
    def update(self, instance, validated_data):
        #instance.update_log(instance, validated_data)
        updated=serializers.HyperlinkedModelSerializer.update(self, instance, validated_data)
        updated.person.update_search_string()
        return updated

class RelationShipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RelationShip
        fields = ('url',  'dt_update',  'dt_obsolete',  'person','retypes', 'destiny')
    
    def create(self, validated_data):
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        created.person.update_search_string()
        created.create_log(created)
        return created
    
    def update(self, instance, validated_data):
        instance.update_log(instance, validated_data)
        updated=serializers.HyperlinkedModelSerializer.update(self, instance, validated_data)
        updated.person.update_search_string()
        return updated

class SearchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Search
        fields = ('url',  'string',  'chips','person')

    def create(self, validated_data):
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        created.person.update_search_string()
        created.create_log(created)
        return created
    
    def update(self, instance, validated_data):
        instance.update_log(instance, validated_data)
        updated=serializers.HyperlinkedModelSerializer.update(self, instance, validated_data)
        updated.person.update_search_string()
        return updated
        
class BlobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Blob
        fields = ('url',  'dt_update','dt_obsolete', 'blob',  'mime', 'name', 'photocontact','person')
        
    def create(self, validated_data):
        request = self.context.get("request")
        if "blob" not in request.FILES:
            print("No file in request")
            return 
        else:
            blob = request.FILES["blob"]
        
        validated_data['blob']=blob.read()
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

    def create(self, validated_data):
        created=serializers.HyperlinkedModelSerializer.create(self,  validated_data)
        created.update_search_string()
        created.create_log(created)
        return created
    
    def update(self, instance, validated_data):
        instance.update_log(instance, validated_data)
        updated=serializers.HyperlinkedModelSerializer.update(self, instance, validated_data)
        updated.update_search_string()
        return updated
    
    class Meta:
        model = Person
        fields = ('dt_update','dt_obsolete','id','url', 'name', 'surname', 'surname2',  'birth', 'death', 'gender', 
        'log', 'alias', 'address', 'relationship', 'phone', 'mail', 'search', 'job', 'group', 'blob')
        
        
class PersonSerializerSearch(serializers.HyperlinkedModelSerializer):
    search = SearchSerializer(many=True,  read_only=True)
    class Meta:
        model = Person
        fields = ('id','url', 'name', 'surname', 'surname2',  'birth', 'death',  'gender',  'search')
        
        
        

