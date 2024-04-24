from django.conf import settings
from django.core.exceptions import ValidationError


def check_username_for_me_value(username: str):
    """Return error if username got "me" value."""
    if username == 'me':
        raise ValidationError(
            message=settings.USER_CREATION_WITH_USERNAME_ME,
            params={'username': username}
        )
