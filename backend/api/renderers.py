import io

from django.conf import settings
from rest_framework.renderers import BaseRenderer


class TextShoppingCartRenderer(BaseRenderer):
    """Render shopping cart as .txt file."""

    media_type = 'text/plain'
    format = 'txt'

    @staticmethod
    def format_ingredients_data(data: list[dict]):
        """Return numerated and formatted ingredients data."""
        return [
            {
                'number': f'{number}.',
                'name': obj.get('ingredients__name').capitalize(),
                'measurement_unit':
                f'({obj.get("ingredients__measurement_unit")})',
                'amount': f'— {obj.get("amount")}'
            }
            for number, obj in enumerate(data, start=1)
        ]

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """Write ingredients data into .txt file."""
        text_buffer = io.StringIO()
        text_buffer.write(
            ' '.join(
                header for header in settings.SHOPPING_CART_FILE_HEADERS
            ) + '\n\n'
        )
        for ingredient_data in data:
            text_buffer.write(
                ' '.join(str(sd) for sd in list(ingredient_data.values()))
                + '\n'
            )
        return text_buffer.getvalue()
