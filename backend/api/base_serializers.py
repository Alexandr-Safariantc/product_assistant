from rest_framework.serializers import ModelSerializer

from recipes.models import Favorite, ShoppingCartRecipe
from users.models import Follow


class GetBoolFieldsSerializer(ModelSerializer):
    """Serializer with get_bool_field_value method."""

    def get_bool_field_value(self, model, current_user, obj):
        """Get bool value for serializer fields."""
        if not current_user.is_authenticated:
            return False
        if model == Favorite or model == ShoppingCartRecipe:
            return model.objects.filter(
                recipe=obj, user=current_user
            ).exists()
        if model == Follow:
            return model.objects.filter(
                following_author=obj, user=current_user
            ).exists()


class ToRepresentationSerializer(ModelSerializer):
    """Serializer with overrided to_representation method."""

    def to_representation(self, instance, serializer):
        """Define serializer class for response."""
        return serializer(
            instance, context={'request': self.context.get('request')}
        ).data
