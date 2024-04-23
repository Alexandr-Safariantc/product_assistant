from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from djoser import utils
from djoser.serializers import TokenSerializer
from djoser.views import TokenCreateView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from foodgram_backend.settings import (
    FOLLOW_RECIPE_DOES_NOT_EXIST,
    SHOP_CART_FAVORITES_RECIPE_TWICE_ADDING_DELETING,
    SUCCESSFULLY_PASSWORD_SETTING
)
from recipes.models import (
    Favorite, Ingredient, Recipe, ShoppingCartRecipe, Tag
)
from users.models import Follow, User
from .custom_viewsets import (
    CreateDestroyListRetrieveModelViewSet, ListRetrieveModelViewSet
)
from .filters import IngredientFilter, RecipeFilter
from .paginators import RecipesPagination, UsersPagination
from .permissions import IsAuthorOrAdminOrSuperuser
from .renderers import TextShoppingCartRenderer
from .serializers import (
    FavoriteShoppingCartRecipeSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipeReadSerializer,
    RecipeSerializer,
    TagSerializer,
    UserPasswordSerializer,
    UserRegistationSerializer,
    UserSerializer,
)


class CustomTokenCreateView(TokenCreateView):
    """Process user authentication token obtaining."""

    def _action(self, serializer):
        """Create and return auth token."""
        return Response(
            data=TokenSerializer(
                utils.login_user(self.request, serializer.user)
            ).data,
            status=status.HTTP_201_CREATED
        )


class IngredientViewSet(ListRetrieveModelViewSet):
    """Process get list of Ingredient instances and get one's detail."""

    queryset = Ingredient.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    """
    Process standard methods with Recipe instances except PUT one.
    Process create, list, retrieve methods with Favorite instances.
    Process create, delete, list methods with ShoppingCartRecipe instances.
    """

    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = RecipesPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrSuperuser
    )
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        """Save value for Recipe author field."""
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,),
        url_name='add_to_or_delete_from_favorites',
        url_path=r'favorite'
    )
    def manage_favorite_recipes(self, request, pk):
        """Add recipe to favorites of request user or delete one."""
        if request.method == 'POST':
            return self.add_recipe(Favorite, request.user, pk)
        else:
            return self.delete_recipe(Favorite, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,),
        url_name='add_to_or_delete_from_shopping_cart',
        url_path=r'shopping_cart'
    )
    def manage_shopping_cart_recipes(self, request, pk):
        """Add recipe to shopping cart of request user or delete one."""
        if request.method == 'POST':
            return self.add_recipe(ShoppingCartRecipe, request.user, pk)
        else:
            return self.delete_recipe(ShoppingCartRecipe, request.user, pk)

    def add_recipe(self, model, current_user, recipe_id):
        """Add recipe to favorites or shopping cart of request user."""
        if model.objects.filter(
            recipe__id=recipe_id, user=current_user
        ).exists():
            return Response(
                data={
                    'error':
                    SHOP_CART_FAVORITES_RECIPE_TWICE_ADDING_DELETING.format(
                        action='добавлен'
                    )},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return Response(
                data={
                    'error': FOLLOW_RECIPE_DOES_NOT_EXIST.format(
                        request_object='Запрашиваемый рецепт'
                    )},
                status=status.HTTP_400_BAD_REQUEST
            )
        model.objects.create(recipe=recipe, user=current_user)
        return Response(
            FavoriteShoppingCartRecipeSerializer(recipe).data,
            status=status.HTTP_201_CREATED
        )

    def delete_recipe(self, model, current_user, recipe_id):
        """Delete recipe from favorites or shopping cart of request user."""
        recipe = model.objects.filter(
            recipe=get_object_or_404(Recipe, id=recipe_id),
            user=current_user
        )
        if recipe.exists():
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            data={
                'error':
                SHOP_CART_FAVORITES_RECIPE_TWICE_ADDING_DELETING.format(
                    action='удален'
                )},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,),
        renderer_classes=[TextShoppingCartRenderer],
        url_name='download_shopping_cart',
        url_path=r'download_shopping_cart'
    )
    def download_shopping_cart(self, request, *args, **kwargs):
        """Download shopping cart of request user as file."""
        queryset = RecipeFilter.filter_shopping_cart_recipes(
            self,
            queryset=self.queryset,
            name='is_in_shopping_cart',
            value=1
        )
        RecipeReadSerializer(
            context={'request': request}, data=queryset, many=True
        ).is_valid()
        all_recipes_ingredients = [
            RecipeReadSerializer.get_ingredients(self, obj=recipe)
            for recipe in queryset
        ]
        all_ingredients = []
        for recipe_ingredients in all_recipes_ingredients:
            for ingredient in recipe_ingredients:
                all_ingredients.append(ingredient)
        unique_ingredients_ids = []
        for ingredient in sorted(
            all_ingredients, key=lambda name: name['name']
        ):
            id = ingredient.get('id')
            if id not in unique_ingredients_ids:
                unique_ingredients_ids.append(id)
        shopping_cart = []
        for number, id in enumerate(unique_ingredients_ids, start=1):
            amount = 0
            unique_ingredient = Ingredient.objects.get(id=id)
            for ingredient in all_ingredients:
                if ingredient.get('id') == id:
                    amount += ingredient.get('amount')
            shopping_cart.append({
                'number': f'{number}.',
                'name': unique_ingredient.name.capitalize(),
                'measurement_unit': f'({unique_ingredient.measurement_unit})',
                'amount': f'— {amount}'
            })
        return Response(
            data=shopping_cart,
            headers={
                'Content-Disposition': 'attachment; '
                f'filename=foodgram_shopping_cart_'
                f'{now():%d-%b_%H-%M}.{(request.accepted_renderer.format)}'
            })


class TagViewSet(ListRetrieveModelViewSet):
    """Process get list of Tag instances and get one's detail."""

    filter_backends = (SearchFilter,)
    queryset = Tag.objects.all()
    search_fields = ('name',)
    serializer_class = TagSerializer


class UserViewSet(CreateDestroyListRetrieveModelViewSet):
    """
    Process create, list, retrieve methods with User instances.
    Process create, delete, list methods with Follow instances.
    """

    filter_backends = (SearchFilter,)
    queryset = User.objects.all()
    pagination_class = UsersPagination
    search_fields = ('username',)

    def get_serializer_class(self):
        """Define serializer for different methods."""
        if self.request.method == 'POST':
            return UserRegistationSerializer
        return UserSerializer

    def perform_create(self, serializer):
        """Hash password before new User instance saving."""
        serializer.validated_data.update({
            'password':
            make_password(serializer.validated_data.get('password'))
        })
        return super().perform_create(serializer)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,),
        url_name='me',
        url_path='me',
    )
    def get_request_user_data(self, request):
        """Get request user data."""
        return Response(
            UserSerializer(request.user, context={'request': request}).data,
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=['post'],
        permission_classes=(IsAuthenticated,),
        url_name='set_password',
        url_path='set_password'
    )
    def set_request_user_password(self, request):
        """Set new password for request user."""
        user = self.request.user
        serializer = UserPasswordSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()
            return Response(
                data={'success': SUCCESSFULLY_PASSWORD_SETTING},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,),
        url_name='subscriptions',
        url_path=r'subscriptions'
    )
    def get_user_subscriptions(self, request, *args, **kwargs):
        """Get authors from request user's subscriptions."""
        return self.get_paginated_response(FollowSerializer(
            self.paginate_queryset(
                User.objects.filter(authors__user=request.user)
            ),
            context={'request': request},
            many=True
        ).data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,),
        url_name='subscribe_or_unsubscribe_author',
        url_path=r'subscribe'
    )
    def manage_subscriptions(self, request, pk):
        """Add author to subscriptions of request user or delete one."""
        current_user = request.user
        author = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            serializer = FollowSerializer(
                author, data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=current_user, following_author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            try:
                Follow.objects.get(
                    following_author=author, user=current_user
                ).delete()
            except Follow.DoesNotExist:
                return Response(
                    data={
                        'error': FOLLOW_RECIPE_DOES_NOT_EXIST.format(
                            request_object='Запрашиваемая подписка'
                        )},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(status=status.HTTP_204_NO_CONTENT)