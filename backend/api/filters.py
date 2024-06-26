from django_filters.rest_framework import filters, FilterSet
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class IngredientFilter(SearchFilter):
    """Describe filter class for IngredientViewSet."""

    search_param = 'name'


class RecipeFilter(FilterSet):
    """Describe filter class for RecipeViewSet."""

    is_favorited = filters.BooleanFilter(
        method='filter_favorite_recipes'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_shopping_cart_recipes'
    )
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )

    class Meta:
        model = Recipe
        fields = (
            'author', 'is_favorited', 'is_in_shopping_cart', 'tags'
        )

    def filter_favorite_recipes(self, queryset, name, value):
        """Get favorite recipes of request user."""
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_shopping_cart_recipes(self, queryset, name, value):
        """Get shopping cart recipes of request user."""
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping_cart_recipes__user=user)
        return queryset
