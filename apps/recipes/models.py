from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.base.models import AuditModel

from apps.users.models import Chef


class RecipeCategory(models.Model):
    """
    Recipe categories
    """
    name = models.CharField(
        verbose_name=_('Category name'),
        max_length=100
    )

    class Meta:
        verbose_name = _('Recipe Category')
        verbose_name_plural = _('Recipe Categories')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Model for ingredients
    """
    name = models.CharField(
        verbose_name=_('Ingredient name'),
        max_length=100
    )
    amount = models.CharField(
        verbose_name=_('Amount of ingredients'),
        max_length=100,
        help_text=_('Open text field to indicate the amount of ingredients')
    )

    def __str__(self) -> str:
        return self.name


class RecipeComplexity(models.IntegerChoices):
    VERY_EASY = 0, _('Very Easy')
    EASY = 1, _('Easy')
    AVERAGE = 2, _('Average')
    DIFFICULT = 3, _('Difficult')
    VERY_DIFFICULT = 4, _('Very Difficult')


class Recipe(AuditModel):
    """
    Model for recipes
    """
    title = models.CharField(
        verbose_name=_('Name'),
        max_length=100
    )
    description = models.TextField(
        verbose_name=_('Description'),
        help_text=_('Description of how to prepare the recipe.')
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name=_('Time'),
        help_text=_('time in minutes needed to cook.'), 
        blank=True, 
        null=True
    )
    servings = models.CharField(
        verbose_name=_('Servings'),
        max_length=100,
        help_text=_('Description of how many plates the recipe serve.')
    )
    procedure_complexity = models.IntegerField(
        verbose_name=_('Complexity'),
        default=RecipeComplexity.AVERAGE, 
        choices=RecipeComplexity.choices
    )
    chef = models.ForeignKey(
        Chef, 
        related_name="recipes",
        on_delete=models.PROTECT
    )
    category = models.ForeignKey(
        RecipeCategory,
        related_name="recipe_list",
        on_delete=models.PROTECT
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name=_('Ingredients')
    )

    class Meta:
        ordering = ('-created_at', )

    def __str__(self) -> str:
        return self.title
