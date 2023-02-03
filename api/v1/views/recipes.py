from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.serializers.recipes import RecipeSerializer, IngredientSerializer, RecipeCategorySerializer
from apps.recipes.models import Recipe, Ingredient, RecipeCategory


class RecipeCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for RecipeCategory's Model
    """
    serializer_class = RecipeCategorySerializer
    queryset = RecipeCategory.objects.filter().order_by('name')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class IngredientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Ingredient's Model
    """
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.filter().order_by('name')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Recipe's Model
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.filter().order_by('-created_at')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    @action(detail=False, methods=['get'], name='search',
    url_path='search', url_name='search')
    def search_recipes(self, request):
        """
        View responsible for search recipes
        """       
        params = self.request.query_params
        _filter = []
        if not params:
            return self.list(request=request)
        
        serializer_context = {
            'request': request,
        }
        if params.get('chef_name', None):
            chef_name = params.get('chef_name', '')
            _filter.append(
                Q(
                    Q(chef__name__icontains=chef_name) |
                    Q(chef__nickname__icontains=chef_name)
                )
            )
        if params.get('chef_id', None):
            _filter.append(
                Q(chef__id=params.get('chef_id', ''))
            )
        if params.get('recipe_title', None):
            _filter.append(
                Q(title__icontains=params.get('recipe_title', ''))
            )
        if params.get('max_time', None):
            _filter.append(
                Q(cooking_time__lte=params.get('max_time', ''))
            )
        if params.get('complexity', None):
            _filter.append(
                Q(procedure_complexity=int(params.get('complexity', '')))
            )
        if params.get('category', None):
            _filter.append(
                Q(category__name__iexact=(params.get('category', '')))
            )

        q_filter = None
        for qf in _filter:
            if not q_filter:
                q_filter = qf
            else:
                q_filter = q_filter & qf
        
        if not q_filter:
            return self.list(request=request)

        queryset = self.queryset.filter(q_filter)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context=serializer_context)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(
            queryset, many=True, context=serializer_context)
        return Response(serializer.data)
