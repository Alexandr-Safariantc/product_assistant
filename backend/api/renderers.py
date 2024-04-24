import io

from django.conf import settings
from rest_framework.renderers import BaseRenderer


class TextShoppingCartRenderer(BaseRenderer):
    """Render shopping cart as .txt file."""

    media_type = 'text/plain'
    format = 'txt'

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
