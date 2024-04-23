from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from foodgram_backend.settings import SUBSCRIBE_TO_SELF
from .models import Follow


@receiver(pre_save, sender=Follow)
def check_self_following(sender, instance: Follow, **kwargs):
    """Return error if follower and following author are the same."""
    if instance.following_author == instance.user:
        raise ValidationError(SUBSCRIBE_TO_SELF)
