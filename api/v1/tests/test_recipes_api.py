from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APIRequestFactory

from apps.recipes.models import Recipe, Ingredient, RecipeCategory
from apps.users.models import Chef
from api.v1.serializers.recipes import RecipeSerializer


factory = APIRequestFactory()
RECIPES_URL = '/api/v1/recipes/'
SEARCH_URL = '/api/v1/recipes/search/'


class RecipesTest(APITestCase):

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
        self.pork_filet = Recipe.objects.create(
            title = "Pork Filet Mignon with Pepper and Pineapple", 
            description = """
                Wash and cut the peppers lengthwise, remove the seeds and white membrane. 
                Place them on a large piece of aluminum foil, season with salt and pepper,
                top with the olive oil, the thyme and the garlic. 
                Close the foil to form an airtight parcel. 
                Bake for about 1 hour at 215ºF. Remove from the oven, cut the peppers into thin strips.
                Peel the pineapple, making sure to keep the soft flesh, cut into cubes. 
                Add to a bowl with the sage leaves; then set aside.
                In a casserole, brown the pork for about 5 minutes in the peanut oil and butter.
                Season with salt and pepper. Add the chopped onions and cook for about 2 minutes, add the peppers. 
                Bake it a casserole dish, uncovered at 350°F.
                Cook for about 8 minutes, then add the pineapple and cook for another 10 minutes. Check the seasoning.
                Cut the fillet and top the vegetables with the meat and the juice created during the cooking.
                For the presentation I added some arugula seasoned with balsamic vinegar.
            """,
            cooking_time = 30,
            servings = "5 people",
            procedure_complexity = 2,
            chef = self.chef_estevam,
            category = self.meat,
        )

        self.roasted_broccoli_soup = Recipe.objects.create(
            title = "Roasted Broccoli Soup", 
            description = """
                Preheat the oven to 400 degrees F (200 degrees C). Line a baking sheet with parchment paper.
                Place broccoli, onion, garlic, and olive oil in a large bowl and toss to coat evenly.
                Place on the prepared baking sheet in a single layer.
                Roast vegetables until soft, 30 to 35 minutes, stirring every 10 minutes.
                Remove from oven. Chop 1/4 cup of broccoli florets; set aside for garnish.
                Combine remaining vegetables with vegetable broth, cream cheese, 
                and lemon pepper in a high-powered blender or food processor in batches. Puree soup until smooth.
                Pour soup into a saucepan over medium-low heat until warmed through, about 5 minutes.
                Season with additional lemon pepper to taste. Ladle into bowls. 
                Garnish with reserved chopped broccoli and crushed red pepper.
            """,
            cooking_time = 55,
            servings = "4 people",
            procedure_complexity = 1,
            chef = self.chef_estevam,
            category = self.vegan,
        )

        self.pork_filet.ingredients.set(
            [
                self.pork_filet_mignon,
                self.pepper,
                self.pineapple
            ]
        )

        self.ingredient_valid = {
        }
        
        self.category_valid = {
        }

        self.recipe_valid = {
            'title': "John Wayne Casserole", 
            'description': """
                Preheat the oven to 350 degrees F (175 degrees C) and lightly grease a 9x13-inch baking pan.
                Place and press biscuit dough into the bottom of the baking pan and halfway up the sides.
                Bake in the preheated oven until lightly browned, 15 to 20 minutes. Leave the oven on.
                Meanwhile, heat a nonstick skillet over medium-high heat and cook ground beef until browned and crumbly,
                about 5 minutes. Drain fat. Stir in taco seasoning and water. Bring to a boil,
                reduce heat, and simmer, stirring occasionally, for 5 minutes. 
                Transfer cooked meat to a bowl and wipe out the skillet.
                Add onion and bell peppers to the same skillet and cook over medium heat until slightly tender, about 5 minutes.           
                Combine sour cream, mayonnaise, 1/2 of the Cheddar cheese, and 1/2 of the onion-pepper mixture in a bowl.
                Layer browned meat, tomatoes, onion-pepper mixture, jalapeño peppers, 
                and sour cream mixture on top of prebaked biscuit dough. Sprinkle with remaining Cheddar cheese.
                Bake uncovered in the preheated oven until cheese is lightly browned and bubbly, 30 to 40 minutes.
            """,
            'cooking_time': 60,
            'servings': "12 people",
            'procedure_complexity': 4,
            'chef': self.chef_estevam.pk,
            'category': self.vegan.pk,
            'ingredients': []
        }

    def test_create_recipe(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'{RECIPES_URL}', self.recipe_valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_recipe_without_authenticated(self):
        response = self.client.post(f'{RECIPES_URL}', self.recipe_valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_chef_with_a_inexistent_category(self):
        self.recipe_valid['category'] = 5
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'{RECIPES_URL}', self.recipe_valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_single_student(self):
        response = self.client.get(f'{RECIPES_URL}{self.pork_filet.pk}/')
        pork_filet = Recipe.objects.get(pk=self.pork_filet.pk)
        serializer = RecipeSerializer(pork_filet)
        self.assertNotEqual(serializer.data, [])
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
  
    def test_update_student_with_put(self):
        self.client.force_authenticate(user=self.user)
        pork_filet = Recipe.objects.get(pk=self.pork_filet.pk)
        pork_filet.title = "Changed title"
        serializer = RecipeSerializer(pork_filet)
        response = self.client.put(f'{RECIPES_URL}{pork_filet.pk}/', serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(pork_filet.title, "Pork Filet Mignon with Pepper and Pineapple")
        self.assertEqual(pork_filet.title, "Changed title")

    def test_delete_recipe(self):
        self.client.force_authenticate(user=self.user)
        pork_filet = Recipe.objects.get(pk=self.pork_filet.pk)
        response = self.client.delete(f'{RECIPES_URL}{pork_filet.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test Search
    def test_search_recipe_without_params(self):
        response = self.client.get(
            f'{SEARCH_URL}'
        )
        recipes = Recipe.objects.filter().order_by('-created_at')

        serializer = RecipeSerializer(recipes, many=True)
        self.assertNotEqual(serializer.data, [])
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_recipe_with_invalid_params(self):
        response = self.client.get(
            f'{SEARCH_URL}?meat=1'
        )
        recipes = Recipe.objects.filter().order_by('-created_at')

        serializer = RecipeSerializer(recipes, many=True)
        self.assertNotEqual(serializer.data, [])
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_recipe_by_chef_name(self):
        chef_name = self.chef_estevam.name
        response = self.client.get(
            f'{SEARCH_URL}?chef_name={chef_name}'
        )
        recipes = Recipe.objects.filter(
            chef__name__icontains=chef_name
        ).order_by('-created_at')

        serializer = RecipeSerializer(recipes, many=True)
        self.assertNotEqual(serializer.data, [])
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_search_by_chef_name_without_recipes(self):
        chef_name = self.chef_gaston.name
        response = self.client.get(
            f'{SEARCH_URL}?chef_name={chef_name}'
        )
        recipes = Recipe.objects.filter(
                chef__name__icontains=chef_name
        ).order_by('-created_at')

        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(serializer.data, [])
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_recipe_by_chef_nickname(self):
        chef_nicknameme = self.chef_estevam.nickname
        response = self.client.get(
            f'{SEARCH_URL}?chef_name={chef_nicknameme}'
        )
        recipes = Recipe.objects.filter(
            chef__nickname__icontains=chef_nicknameme
        ).order_by('-created_at')

        serializer = RecipeSerializer(recipes, many=True)
        self.assertNotEqual(serializer.data, [])
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)   

    def test_search_recipe_by_chef_id(self):
        chef_id = self.chef_estevam.id
        response = self.client.get(
            f'{SEARCH_URL}?chef_id={chef_id}&'
        )
        recipes = Recipe.objects.filter(
            chef_id=chef_id
        ).order_by('-created_at')

        serializer = RecipeSerializer(recipes, many=True)
        self.assertNotEqual(serializer.data, [])
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_search_recipe_by_recipe_title(self):
        title = self.roasted_broccoli_soup.title
        response = self.client.get(
            f'{SEARCH_URL}?recipe_title={title}&'
        )
        recipes = Recipe.objects.filter(
            title__icontains=title
        ).order_by('-created_at')

        serializer = RecipeSerializer(recipes, many=True)
        self.assertNotEqual(serializer.data, [])
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        
    def test_search_recipe_by_recipe_parcial_title(self):
        title = 'Por'
        response = self.client.get(
            f'{SEARCH_URL}?recipe_title={title}&'
        )
        recipes = Recipe.objects.filter(
            title__icontains=title
        ).order_by('-created_at')

        serializer = RecipeSerializer(recipes, many=True)
        self.assertNotEqual(serializer.data, [])
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_search_recipe_by_max_time(self):
        max_time = 45
        response = self.client.get(
            f'{SEARCH_URL}?max_time={max_time}&'
        )
        recipes = Recipe.objects.filter(
            cooking_time__lte=max_time
        ).order_by('-created_at')

        serializer = RecipeSerializer(recipes, many=True)
        self.assertNotEqual(serializer.data, [])
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
    

    def test_search_recipe_by_procedure_complexity(self):
        complexity = 2
        response = self.client.get(
            f'{SEARCH_URL}?complexity={complexity}&'
        )
        recipes = Recipe.objects.filter(
            procedure_complexity=complexity
        ).order_by('-created_at')

        serializer = RecipeSerializer(recipes, many=True)
        self.assertNotEqual(serializer.data, [])
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
    
    def test_search_recipe_by_category_name(self):
        category_name = self.vegan.name
        response = self.client.get(
            f'{SEARCH_URL}?category={category_name}&'
        )
        recipes = Recipe.objects.filter(
            category__name__iexact=category_name
        ).order_by('-created_at')

        serializer = RecipeSerializer(recipes, many=True)
        self.assertNotEqual(serializer.data, [])
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_search_recipe_by_category_name_and_chef_name(self):
        category_name = self.vegan.name
        chef_name = self.chef_estevam.name
        response = self.client.get(
            f'{SEARCH_URL}?category={category_name}&chef_name={chef_name}'
        )
        recipes = Recipe.objects.filter(
            Q(
                Q(category__name__iexact=category_name) &
                Q(chef__name__icontains=chef_name)
            )
        ).order_by('-created_at')

        serializer = RecipeSerializer(recipes, many=True)
        self.assertNotEqual(serializer.data, [])
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
