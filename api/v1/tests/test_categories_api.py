from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APIRequestFactory

from apps.recipes.models import RecipeCategory
from apps.users.models import Chef
from api.v1.serializers.recipes import RecipeCategorySerializer


factory = APIRequestFactory()
CATEGORIES_URL = '/api/v1/categories/'


class RecipeCategorysTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username = 'chef_user',
            password = 'password159'
        )

        self.user_secondary = get_user_model().objects.create_user(
            username = 'chef_user_secondary',
            password = 'password159'
        )

        self.chef_estevam = Chef.objects.create(
            name = "Dom Estevam", 
            nickname = "Mr. Estavam", 
            description = "Chef of Rest's restaurant", 
            user = self.user
        )
        self.chef_gaston = Chef.objects.create(
            name = "Dom Gaston", 
            nickname = "Mr. Gaston", 
            description = "Chef of Gastons's restaurant", 
            user = self.user_secondary
        )

        self.meat = RecipeCategory.objects.create(
            name = "Meat", 
        )

        self.vegan = RecipeCategory.objects.create(
            name = "Vegan", 
        )

        self.category_valid = {
            "name": "Chicken", 
        }

    def test_create_category(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'{CATEGORIES_URL}', self.category_valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_category_without_authenticated(self):
        response = self.client.post(f'{CATEGORIES_URL}', self.category_valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_single_category(self):
        response = self.client.get(f'{CATEGORIES_URL}{self.meat.pk}/')
        meat = RecipeCategory.objects.get(pk=self.meat.pk)
        serializer = RecipeCategorySerializer(meat)
        self.assertNotEqual(serializer.data, [])
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
  
    def test_update_category_with_put(self):
        self.client.force_authenticate(user=self.user)
        meat = RecipeCategory.objects.get(pk=self.meat.pk)
        meat.name = "Changed name"
        serializer = RecipeCategorySerializer(meat)
        response = self.client.put(f'{CATEGORIES_URL}{meat.pk}/', serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(meat.name, "Pork Filet Mignon")
        self.assertEqual(meat.name, "Changed name")

    def test_delete_category(self):
        self.client.force_authenticate(user=self.user)
        meat = RecipeCategory.objects.get(pk=self.meat.pk)
        response = self.client.delete(f'{CATEGORIES_URL}{meat.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
