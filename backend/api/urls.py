from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredient')
router_v1.register(r'recipes', RecipeViewSet, basename='recipe')
router_v1.register(r'tags', TagViewSet, basename='tag')
router_v1.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls)),
]
