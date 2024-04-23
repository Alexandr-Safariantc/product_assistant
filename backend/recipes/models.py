from colorfield.fields import ColorField
from django.db import models

from foodgram_backend.settings import (
    INGREDIENT_NAME_MAX_LENGTH,
    MEASUREMENT_NAME_MAX_LENGTH,
    RECIPE_NAME_MAX_LENGTH,
    TAG_NAME_SLUG_MAX_LENGTH
)
from users.models import User
from .validators import validate_cooking_time, validate_ingredient_amount


class Ingredient(models.Model):
    """Describe ingredient model."""

    name = models.CharField(
        'Название', db_index=True, max_length=INGREDIENT_NAME_MAX_LENGTH,
    )
    measurement_unit = models.CharField(
        'Единица измерения', max_length=MEASUREMENT_NAME_MAX_LENGTH
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit'
            )
        ]
        default_related_name = 'ingredients'
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
        max_length=TAG_NAME_SLUG_MAX_LENGTH,
        unique=True
    )
    color = ColorField('Цветовой код (Hex)', default='#FF0000')
    slug = models.SlugField(
        'Идентификатор',
        db_index=True,
        max_length=TAG_NAME_SLUG_MAX_LENGTH,
        unique=True
    )

    class Meta:
        default_related_name = 'tags'
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
    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)',
        validators=[validate_cooking_time, ]
    )
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    image = models.ImageField('Картинка', upload_to='recipes/images/')
    name = models.CharField(
        'Название', db_index=True, max_length=RECIPE_NAME_MAX_LENGTH
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

    amount = models.IntegerField(
        'Количество ингридиента', validators=[validate_ingredient_amount, ]
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

    def __str__(self):
        """Return instance text representation."""
        return f'Тег: {self.tag} для рецепта: {self.recipe}'


class Favorite(models.Model):
    """Describe favorite recipes of users."""

    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites_owners',
        verbose_name='Пользователь'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_favorite_recipe'
            )
        ]
        ordering = ('-created_at', 'recipe__name')
        verbose_name = 'избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        """Return instance text representation."""
        return (f'Избранный рецепт: {self.recipe}'
                f' пользователя: {self.user}')


class ShoppingCartRecipe(models.Model):
    """Describe recipes of users' shopping cart."""

    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes_to_buy',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_owners',
        verbose_name='Пользователь'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_shopping_cart_recipe'
            )
        ]
        ordering = ('-created_at', 'recipe__name',)
        verbose_name = 'список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        """Return instance text representation."""
        return (f'Рецепт {self.recipe} из списка покупок'
                f' пользователя: {self.user}')
