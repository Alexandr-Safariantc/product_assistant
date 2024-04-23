from django.contrib.auth.password_validation import validate_password
from django.db.models import F
from django.db.transaction import atomic
from djoser.serializers import TokenCreateSerializer
from rest_framework import serializers

from foodgram_backend.settings import (
    EMAIL_FIELD_MAX_LENGTH,
    INVALID_CURRENT_PASSWORD_VALUE,
    PASSWORD_FIELD_MAX_LENGTH,
    RECIPE_CREATION_WITH_DUPLICATE_INGREDIENTS_TAGS,
    RECIPE_CREATION_WITHOUT_INGREDIENTS_TAGS,
    SUBSCRIBE_TWICE_TO_SAME_AUTHOR,
    SUBSCRIBE_TO_SELF,
)
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCartRecipe,
    Tag,
    TagRecipe
)
from recipes.validators import validate_ingredient_amount
from users.models import Follow, User
from .custom_fields import Base64ImageField
from .custom_serializers import CustomSerializer


class CustomTokenCreateSerializer(TokenCreateSerializer):
    """Process token creation by getting email, password values."""

    email = serializers.EmailField(max_length=EMAIL_FIELD_MAX_LENGTH)
    password = serializers.CharField(
        max_length=PASSWORD_FIELD_MAX_LENGTH,
        style={'input_type': 'password'},
        validators=[validate_password,],
    )


class FavoriteShoppingCartRecipeSerializer(serializers.ModelSerializer):
    """
    Process create and delete methods with
    Favorite and ShoppingCartRecipe instances.
    """

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'cooking_time', 'image', 'name')


class IngredientSerializer(serializers.ModelSerializer):
    """Process get list of Ingredient instances and get one's detail."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Process create and update IngredientRecipe instances."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(validators=[validate_ingredient_amount,])

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class TagSerializer(serializers.ModelSerializer):
    """Process get list of Tag instances and get one's detail."""

    class Meta:
        model = Tag
        fields = '__all__'


class UserPasswordSerializer(serializers.Serializer):
    """Process user's password changing."""

    current_password = serializers.CharField(
        max_length=PASSWORD_FIELD_MAX_LENGTH,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        max_length=PASSWORD_FIELD_MAX_LENGTH,
        style={'input_type': 'password'},
        validators=[validate_password,]
    )

    def validate_current_password(self, current_password):
        """
        Return error if current_password value
        and user's password from db are not the same.
        """
        if not self.context.get('request').user.check_password(
            current_password
        ):
            raise serializers.ValidationError(
                {'error': INVALID_CURRENT_PASSWORD_VALUE}
            )
        return current_password


class UserRegistationSerializer(serializers.ModelSerializer):
    """Process new User instance creation."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'first_name',
            'last_name',
            'password',
            'username'
        )
        extra_kwargs = {'password': {
            'style': {'input_type': 'password'},
            'write_only': True
        }}
        read_only_fields = ('id',)


class UserSerializer(CustomSerializer):
    """Process list and retrieve methods with User instances."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'is_subscribed',
            'first_name',
            'last_name',
            'username'
        )

    def get_is_subscribed(self, obj):
        """
        Return True if current user is subscribed
        to requested user, False otherwise.
        """
        return self.get_bool_field_value(
            Follow, self.context.get('request').user, obj
        )


class FollowSerializer(UserSerializer):
    """Process get, create and delete methods with Follow instances."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')
        read_only_fields = UserSerializer.Meta.fields

    def get_recipes(self, obj):
        """Get recipes of following author."""
        recipes = obj.recipes.all()
        recipes_limit = self.context.get('request').GET.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        serializer = FavoriteShoppingCartRecipeSerializer(
            recipes, many=True, read_only=True
        )
        return serializer.data

    def get_recipes_count(self, obj):
        """Get following author's recipes amount."""
        return obj.recipes.count()

    def validate(self, data):
        """Check field values for duplicate and self subscriptions."""
        author = self.instance
        user = self.context.get('request').user
        if author == user:
            raise serializers.ValidationError({'error': SUBSCRIBE_TO_SELF})
        if Follow.objects.filter(following_author=author, user=user).exists():
            raise serializers.ValidationError(
                {'error': SUBSCRIBE_TWICE_TO_SAME_AUTHOR},
            )
        return data


class RecipeReadSerializer(CustomSerializer):
    """Process safety methods with Recipe instances."""

    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'cooking_time',
            'ingredients',
            'image',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'tags',
            'text',
        )
        read_only_fields = (
            'id', 'is_favorited', 'is_in_shopping_cart'
        )

    def get_ingredients(self, obj):
        """Get recipe's ingridients info."""
        return obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('ingredientrecipe__amount')
        )

    def get_is_favorited(self, obj):
        """
        Return True if current user added requested recipe
        to favorites, False otherwise.
        """
        return self.get_bool_field_value(
            Favorite, self.context.get('request').user, obj
        )

    def get_is_in_shopping_cart(self, obj):
        """
        Return True if current user added requested recipe
        to shopping cart, False otherwise.
        """
        return self.get_bool_field_value(
            ShoppingCartRecipe, self.context.get('request').user, obj
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Process non-safety methods with Recipe instances except PUT one."""

    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = IngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'cooking_time',
            'ingredients',
            'image',
            'name',
            'tags',
            'text',
        )
        read_only_fields = ('id',)

    def validate_tags(self, tags):
        """Check tags field value for non-emptyness and uniqueness."""
        if not tags:
            raise serializers.ValidationError({
                'error':
                RECIPE_CREATION_WITHOUT_INGREDIENTS_TAGS.format(
                    field_name='тег'
                )
            })
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError({
                'error':
                RECIPE_CREATION_WITH_DUPLICATE_INGREDIENTS_TAGS.format(
                    field_name='тег'
                )
            })
        return tags

    def validate_ingredients(self, ingredients):
        """Check ingredients field value for non-emptyness and uniqueness."""
        if not ingredients:
            raise serializers.ValidationError({
                'error': RECIPE_CREATION_WITHOUT_INGREDIENTS_TAGS.format(
                    field_name='ингредиент'
                )
            })
        unique_values = []
        for ingredient in ingredients:
            if ingredient in unique_values:
                raise serializers.ValidationError({
                    'error':
                    RECIPE_CREATION_WITH_DUPLICATE_INGREDIENTS_TAGS.format(
                        field_name='ингредиент'
                    )
                })
            unique_values.append(ingredient)
        return ingredients

    def validate(self, data):
        """Check fields request values."""
        self.validate_ingredients(data.get('ingredients'))
        self.validate_tags(data.get('tags'))
        return super().validate(data)

    @atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            TagRecipe.objects.create(
                tag=tag, recipe=recipe
            )
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                amount=ingredient.get('amount'),
                ingredient=ingredient.get('id'),
                recipe=recipe
            )
        return recipe

    @atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        updated_ingredients = []
        for ingredient in ingredients:
            updated_ingredients.append(ingredient.get('id'))
        instance.ingredients.set(updated_ingredients)
        instance.tags.set(tags)
        instance.save()
        return instance

    def to_representation(self, instance):
        """Define serializer class for response."""
        return RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data
