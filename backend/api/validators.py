from django.conf import settings
from rest_framework import serializers


class SelfSubscriptionValidator:
    """Check field values for self subscriptions."""
    message = settings.SUBSCRIBE_TO_SELF

    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message or self.message

    def __call__(self, attrs):
        if attrs.get('following_author') == attrs.get('user'):
            raise serializers.ValidationError({'error': self.message})
