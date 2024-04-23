from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
)
from rest_framework.viewsets import GenericViewSet


class ListRetrieveModelViewSet(
    ListModelMixin, RetrieveModelMixin, GenericViewSet,
):
    """Mixin for list and retrieve methods, contains SearchFilter."""

    pass


class CreateDestroyListRetrieveModelViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListRetrieveModelViewSet,
):
    """Mixin for create, delete, list and retrieve methods."""

    pass
