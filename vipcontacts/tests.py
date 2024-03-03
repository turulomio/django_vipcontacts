from django.contrib.auth.models import User
from django.test import tag
from django.utils import timezone
from json import loads
from vipcontacts.reusing import tests_helpers
from vipcontacts import models
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

tag

class CtTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        """
            Only instantiated once
        """
        super().setUpClass()
        
        # User to test api
        cls.user_authorized_1 = User(
            email='testing@testing.com',
            first_name='Testing',
            last_name='Testing',
            username='testing',
        )
        cls.user_authorized_1.set_password('testing123')
        cls.user_authorized_1.save()
        
        # User to confront security
        cls.user_authorized_2 = User(
            email='other@other.com',
            first_name='Other',
            last_name='Other',
            username='other',
        )
        cls.user_authorized_2.set_password('other123')
        cls.user_authorized_2.save()
        
        client = APIClient()
        response = client.post('/login/', {'username': cls.user_authorized_1.username, 'password': 'testing123',},format='json')
        result = loads(response.content)
        cls.token_user_authorized_1 = result
        
        response = client.post('/login/', {'username': cls.user_authorized_2.username, 'password': 'other123',},format='json')
        result = loads(response.content)
        cls.token_user_authorized_2 = result
        
        cls.client_authorized_1=APIClient()
        cls.client_authorized_1.credentials(HTTP_AUTHORIZATION='Token ' + cls.token_user_authorized_1)
        cls.client_authorized_1.user=cls.user_authorized_1
        
        cls.client_anonymous=APIClient()
        cls.client_anonymous.user=None

        cls.now=timezone.now()

    def test_person(self):
        tests_helpers.client_post(self, self.client_authorized_1, "/api/person/", models.Person.post_payload(), status.HTTP_201_CREATED) #Removes one share
        tests_helpers.common_actions_tests(self,  self.client_authorized_1, "/api/person/", models.Person.post_payload(), 1, post=status.HTTP_201_CREATED, delete=status.HTTP_204_NO_CONTENT)
        dict_person_search=tests_helpers.client_get(self, self.client_authorized_1,  "/api/person/?search=turu", status.HTTP_200_OK)
        self.assertEqual(len(dict_person_search), 1 )        
        dict_person_last_editions=tests_helpers.client_get(self, self.client_authorized_1,  "/api/person/?search=:LAST 30", status.HTTP_200_OK)
        self.assertEqual(len(dict_person_last_editions), 1 )

    def test_address(self):
        dict_person=tests_helpers.client_post(self, self.client_authorized_1, "/api/person/", models.Person.post_payload(), status.HTTP_201_CREATED) #Removes one share
        tests_helpers.common_actions_tests(self,  self.client_authorized_1, "/api/address/", models.Address.post_payload(person=dict_person["url"]), 1, post=status.HTTP_201_CREATED, delete=status.HTTP_204_NO_CONTENT)


    def test_alias(self):
        dict_person=tests_helpers.client_post(self, self.client_authorized_1, "/api/person/", models.Person.post_payload(), status.HTTP_201_CREATED) #Removes one share
        tests_helpers.common_actions_tests(self,  self.client_authorized_1, "/api/alias/", models.Alias.post_payload(person=dict_person["url"]), 1, post=status.HTTP_201_CREATED, delete=status.HTTP_204_NO_CONTENT)

                
    def test_group(self):
        dict_person=tests_helpers.client_post(self, self.client_authorized_1, "/api/person/", models.Person.post_payload(), status.HTTP_201_CREATED) #Removes one share
        tests_helpers.common_actions_tests(self,  self.client_authorized_1, "/api/group/", models.Group.post_payload(person=dict_person["url"]), 1, post=status.HTTP_201_CREATED, delete=status.HTTP_204_NO_CONTENT)

    @tag("current")
    def test_person_changes(self):
        person=models.Person(name="Turulomio", gender=1)
        person.save()
        person.lod_changes(console=True)
    
    
    def test_job(self):
        dict_person=tests_helpers.client_post(self, self.client_authorized_1, "/api/person/", models.Person.post_payload(), status.HTTP_201_CREATED) #Removes one share
        tests_helpers.common_actions_tests(self,  self.client_authorized_1, "/api/job/", models.Job.post_payload(person=dict_person["url"]), 1, post=status.HTTP_201_CREATED, delete=status.HTTP_204_NO_CONTENT)

            

    def test_log(self):
        dict_person=tests_helpers.client_post(self, self.client_authorized_1, "/api/person/", models.Person.post_payload(), status.HTTP_201_CREATED) #Removes one share
        dict_log=tests_helpers.client_post(self, self.client_authorized_1, "/api/log/", models.Log.post_payload(person=dict_person["url"]), status.HTTP_201_CREATED) #Removes one share
        tests_helpers.common_actions_tests(self,  self.client_authorized_1, "/api/log/", models.Log.post_payload(person=dict_person["url"]), dict_log["id"], post=status.HTTP_201_CREATED, delete=status.HTTP_204_NO_CONTENT)

