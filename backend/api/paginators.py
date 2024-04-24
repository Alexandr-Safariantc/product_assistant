from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class RecipesPagination(PageNumberPagination):
    """
    Custom paginator for Recipe instances views,
    is setted by parameters from settings.py.
    """

    page_size = settings.RECIPES_PAGE_SIZE
    page_size_query_param = settings.QUERY_PARAMETER_NAME
    max_page_size = settings.MAX_PAGE_SIZE


class UsersPagination(PageNumberPagination):
    """
    Custom paginator for User instances views,
    is setted by parameters from settings.py.
    """

    page_size = settings.USERS_PAGE_SIZE
    page_size_query_param = settings.QUERY_PARAMETER_NAME
    max_page_size = settings.MAX_PAGE_SIZE
