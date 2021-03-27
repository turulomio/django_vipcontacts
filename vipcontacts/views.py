from rest_framework import viewsets
from rest_framework import permissions

from vipcontacts.models import Person
from vipcontacts.serializers import PersonSerializer

class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Person.objects.all().order_by('name')
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]
