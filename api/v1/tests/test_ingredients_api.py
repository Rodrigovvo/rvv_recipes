
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APIRequestFactory

from apps.recipes.models import Ingredient
from apps.users.models import Chef
from api.v1.serializers.recipes import IngredientSerializer


factory = APIRequestFactory()
INGREDIENTS_URL = '/api/v1/ingredients/'



class IngredientsTest(APITestCase):

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

        self.pork_filet_mignon = Ingredient.objects.create(
            name = "Pork Filet Mignon", 
            amount = "1 kg"
        )

        self.pepper = Ingredient.objects.create(
            name = "Pepper", 
            amount = "3 g"
        )

        self.pineapple = Ingredient.objects.create(
            name = "Pineapple", 
            amount = "100 g"
        )

        self.ingredient_valid = {
            "name": "Rice", 
            "amount": "200 g"
        }

    def test_create_ingredient(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'{INGREDIENTS_URL}', self.ingredient_valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_ingredient_without_authenticated(self):
        response = self.client.post(f'{INGREDIENTS_URL}', self.ingredient_valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_single_ingredient(self):
        response = self.client.get(f'{INGREDIENTS_URL}{self.pork_filet_mignon.pk}/')
        pork_filet_mignon = Ingredient.objects.get(pk=self.pork_filet_mignon.pk)
        serializer = IngredientSerializer(pork_filet_mignon)
        self.assertNotEqual(serializer.data, [])
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
  
    def test_update_ingredient_with_put(self):
        self.client.force_authenticate(user=self.user)
        pork_filet_mignon = Ingredient.objects.get(pk=self.pork_filet_mignon.pk)
        pork_filet_mignon.name = "Changed name"
        serializer = IngredientSerializer(pork_filet_mignon)
        response = self.client.put(f'{INGREDIENTS_URL}{pork_filet_mignon.pk}/', serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(pork_filet_mignon.name, "Pork Filet Mignon")
        self.assertEqual(pork_filet_mignon.name, "Changed name")

    def test_delete_ingredient(self):
        self.client.force_authenticate(user=self.user)
        pork_filet_mignon = Ingredient.objects.get(pk=self.pork_filet_mignon.pk)
        response = self.client.delete(f'{INGREDIENTS_URL}{pork_filet_mignon.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
