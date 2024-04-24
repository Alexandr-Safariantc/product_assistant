from django.conf import settings
from django.contrib import admin

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCartRecipe,
    Tag,
    TagRecipe
)


class FavoriteInline(admin.StackedInline):
    model = Favorite
    extra = 0


class IngredientRecipeInline(admin.StackedInline):
    model = IngredientRecipe
    extra = 0


class TagRecipeInline(admin.StackedInline):
    model = TagRecipe
    extra = 0


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'created_at',)
    list_filter = ('user__username',)
    search_fields = ('user__username', 'recipe_name')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_editable = ('measurement_unit',)
    list_filter = ('measurement_unit',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (FavoriteInline, IngredientRecipeInline, TagRecipeInline)
    list_display = (
        'author',
        'name',
        'cooking_time',
        'created_at',
    )
    list_editable = ('name',)
    list_filter = ('author', 'name', 'ingredients', 'tags')
    search_fields = ('author', 'name', 'ingredients', 'tags')


@admin.register(ShoppingCartRecipe)
class ShoppingCartRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'created_at',)
    list_filter = ('user',)
    search_fields = ('user', 'recipe')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color',)
    list_editable = ('slug', 'color',)
    list_filter = ('name', 'slug', 'color',)
    search_fields = ('name', 'slug', 'color',)


admin.site.empty_value_display = settings.ADMIN_SITE_EMPTY_VALUE
