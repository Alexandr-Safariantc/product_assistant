from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class RecipesPagination(PageNumberPagination):
    """Pagination for Recipe instances views."""

    page_size = settings.RECIPES_PAGE_SIZE
    page_size_query_param = settings.QUERY_PARAMETER_NAME
    max_page_size = settings.MAX_PAGE_SIZE


class UsersPagination(PageNumberPagination):
    """Pagination for User instances views."""

    page_size = settings.USERS_PAGE_SIZE
    page_size_query_param = settings.QUERY_PARAMETER_NAME
    max_page_size = settings.MAX_PAGE_SIZE
