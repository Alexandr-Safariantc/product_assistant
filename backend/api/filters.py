from django_filters.rest_framework import filters, FilterSet

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):
    """Describe filter class for IngredientViewSet."""

    name = filters.CharFilter()

    class Meta:
        model = Ingredient
        fields = {
            'name': ['istartswith', 'icontains']
        }


class RecipeFilter(FilterSet):
    """Describe filter class for RecipeViewSet."""

    is_favorited = filters.BooleanFilter(
        method='filter_favorite_recipes'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_shopping_cart_recipes'
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)

    def filter_favorite_recipes(self, queryset, name, value):
        """Get favorite recipes of request user."""
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_shopping_cart_recipes(self, queryset, name, value):
        """Get shopping cart recipes of request user."""
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(recipes_to_buy__user=user)
        return queryset
