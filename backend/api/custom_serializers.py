from rest_framework.serializers import ModelSerializer

from recipes.models import Favorite, ShoppingCartRecipe
from users.models import Follow


class CustomSerializer(ModelSerializer):
    """Serializer with get_bool_field_value method."""

    def get_bool_field_value(self, model, current_user, obj):
        """
        Get bool value for is_subscribed, is_favorited,
        is_in_shopping_cart fields.
        """
        if current_user.is_anonymous:
            return False
        if model == Favorite or model == ShoppingCartRecipe:
            return model.objects.filter(
                recipe=obj, user=current_user
            ).exists()
        if model == Follow:
            return model.objects.filter(
                following_author=obj, user=current_user
            ).exists()
