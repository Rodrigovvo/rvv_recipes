from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.recipes.models import RecipeCategory, Ingredient, Recipe


class RecipeCategorySerializer(serializers.ModelSerializer):
    """ Serializer for Recipe Category """
    class Meta:
        model = RecipeCategory
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """ Serializer for Ingredient """
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer for Recipe """
    ingredients = IngredientSerializer(many=True, read_only=True)
    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'cooking_time', 'servings',
            'procedure_complexity','chef', 'category', 'ingredients', 
        ]
