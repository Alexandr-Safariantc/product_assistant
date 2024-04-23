from rest_framework.pagination import PageNumberPagination

from foodgram_backend.settings import (
    QUERY_PARAMETER_NAME, MAX_PAGE_SIZE, RECIPES_PAGE_SIZE, USERS_PAGE_SIZE
)


class RecipesPagination(PageNumberPagination):
    """
    Custom paginator for Recipe instances views,
    is setted by parameters from settings.py.
    """

    page_size = RECIPES_PAGE_SIZE
    page_size_query_param = QUERY_PARAMETER_NAME
    max_page_size = MAX_PAGE_SIZE


class UsersPagination(PageNumberPagination):
    """
    Custom paginator for User instances views,
    is setted by parameters from settings.py.
    """

    page_size = USERS_PAGE_SIZE
    page_size_query_param = QUERY_PARAMETER_NAME
    max_page_size = MAX_PAGE_SIZE
