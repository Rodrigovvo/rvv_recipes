from imp import SEARCH_ERROR
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from apps.users.models import Chef
from api.v1.serializers.users import ChefSerializer


factory = APIRequestFactory()
CHEF_URL = '/api/v1/chefs/'

class ChefTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username = 'chef_user',
            password = 'password159'
        )

        self.chef_estevam = Chef.objects.create(
            name= "Dom Estevam", 
            nickname= "Mr. Estavam", 
            description= "Chef of Rest's restaurant", 
            user= self.user
        )

        self.valid = {
            "name": "Dom Ramon", 
            "nickname": "Mr. Madruga", 
            "description": "Chef of Da Vila's restaurant", 
            "user": 1
            }

    def test_create_chef(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'{CHEF_URL}', self.valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_chef_without_authenticated(self):
        response = self.client.post(f'{CHEF_URL}', self.valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_chef_with_name_longer_than_limit(self):
        self.valid['name'] = """
             Pedro de Alcântara João Carlos Leopoldo Salvador 
             Bibiano Francisco Xavier de Paula Leocádio Miguel Gabriel 
             Rafael Gonzaga da Silva
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'{CHEF_URL}', self.valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_chef_without_user(self):
        self.valid.pop('user')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'{CHEF_URL}', self.valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_chef_with_user_equal_none(self):
        self.valid['user'] = None
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'{CHEF_URL}', self.valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_single_student(self):
        response = self.client.get(f'{CHEF_URL}{self.chef_estevam.pk}/')
        chef_estevam = Chef.objects.get(pk=self.chef_estevam.pk)
        serializer = ChefSerializer(chef_estevam)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
  
    def test_update_student_with_put(self):
        self.client.force_authenticate(user=self.user)
        chef = Chef.objects.get(pk=self.chef_estevam.pk)
        chef.description = "Chef of Da Vila's restaurant"
        serializer = ChefSerializer(chef)
        response = self.client.put(f'{CHEF_URL}{chef.pk}/', serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(chef.description, "Chef of Rest's restaurant")
        self.assertEqual(chef.description,  "Chef of Da Vila's restaurant")

    def test_update_student_without_authentication(self):
        chef = Chef.objects.get(pk=self.chef_estevam.pk)
        chef.description = "Chef of Da Vila's restaurant"
        serializer = ChefSerializer(chef)
        response = self.client.put(f'{CHEF_URL}{chef.pk}/', serializer.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_soft_delete_chef(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'{CHEF_URL}{self.chef_estevam.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        chef = Chef.objects.get(pk=self.chef_estevam.pk)
        self.assertEqual(chef.active, False)
