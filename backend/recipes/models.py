from colorfield.fields import ColorField
from django.conf import settings
from django.db import models

from recipes.validators import (
    validate_cooking_time, validate_ingredient_amount
)
from recipes.utils import get_random_hex_code
from users.models import User


class Ingredient(models.Model):
    """Describe ingredient model."""

    name = models.CharField(
        'Название',
        max_length=settings.INGREDIENT_NAME_MEASURE_MAX_LENGTH,
        db_index=True
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=settings.INGREDIENT_NAME_MEASURE_MAX_LENGTH
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit'
            )
        ]
        ordering = ('name',)
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        """Return instance text representation."""
        return f'Ингредиент: {self.name}'


class Tag(models.Model):
    """Describe tag model."""

    name = models.CharField(
        'Название',
        db_index=True,
        max_length=settings.TAG_NAME_SLUG_MAX_LENGTH,
        unique=True
    )
    color = ColorField(
        'Цветовой код (Hex)', default=get_random_hex_code, unique=True
    )
    slug = models.SlugField(
        'Идентификатор',
        db_index=True,
        max_length=settings.TAG_NAME_SLUG_MAX_LENGTH,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        """Return instance text representation."""
        return f'Тег: {self.name}'


class Recipe(models.Model):
    """Describe recipe model."""

    author = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления (в минутах)',
        validators=[validate_cooking_time]
    )
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    image = models.ImageField('Картинка', upload_to='recipes/images/')
    name = models.CharField(
        'Название', db_index=True, max_length=settings.RECIPE_NAME_MAX_LENGTH
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Список ингредиентов'
    )
    tags = models.ManyToManyField(
        Tag, through='TagRecipe', verbose_name='Теги'
    )
    text = models.TextField('Описание')

    class Meta:
        default_related_name = 'recipes'
        ordering = ('-created_at', 'name')
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        """Return instance text representation."""
        return f'Рецепт: {self.name}'


class IngredientRecipe(models.Model):
    """Linked model for ingredient - recipe relation."""

    amount = models.PositiveSmallIntegerField(
        'Количество ингридиента', validators=[validate_ingredient_amount]
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]
        default_related_name = 'ingredients_recipes'
        ordering = ('ingredient__name', 'recipe__name')
        verbose_name = 'ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецептов'

    def __str__(self):
        """Return instance text representation."""
        return f'Ингредиент: {self.ingredient} для рецепта: {self.recipe}'


class TagRecipe(models.Model):
    """Linked model for tag - recipe relation."""

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт'
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Тег')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'recipe'], name='unique_tag_recipe'
            )
        ]
        default_related_name = 'tags_recipes'
        ordering = ('tag__name', 'recipe__name')
        verbose_name = 'тег рецепта'
        verbose_name_plural = 'Теги рецептов'

    def __str__(self):
        """Return instance text representation."""
        return f'Тег: {self.tag} для рецепта: {self.recipe}'


class CreateTimeRecipeUserModel(models.Model):
    """Describe created_at, recipe-related, user-related fields."""

    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь'
    )

    class Meta:
        abstract = True
        ordering = ('-created_at', 'recipe__name')

    def __str__(self, group_name):
        """Return instance text representation."""
        return (f'Рецепт {self.recipe} из {group_name}'
                f' пользователя: {self.user}')


class Favorite(CreateTimeRecipeUserModel):
    """Describe favorite recipes of users."""

    class Meta:
        default_related_name = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_favorite_recipe'
            )
        ]
        verbose_name = 'избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self, group_name='избранного'):
        return super().__str__(group_name)


class ShoppingCartRecipe(CreateTimeRecipeUserModel):
    """Describe recipes of users' shopping cart."""

    class Meta:
        default_related_name = 'shopping_cart_recipes'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_shopping_cart_recipe'
            )
        ]
        verbose_name = 'список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self, group_name='списка покупок'):
        return super().__str__(group_name)
