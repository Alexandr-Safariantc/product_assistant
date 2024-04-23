from django.contrib import admin

from foodgram_backend.settings import ADMIN_SITE_EMPTY_VALUE
from .models import Follow, User


class FollowInline(admin.StackedInline):
    model = Follow
    extra = 0
    fk_name = 'following_author'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following_author', 'created_at',)
    list_editable = ('following_author',)
    list_filter = ('user', 'following_author')
    search_fields = ('user', 'following_author')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (FollowInline,)
    list_display = (
        'username',
        'email',
        'role',
        'is_active',
        'last_login',
        'date_joined',
    )
    list_editable = ('role',)
    list_filter = ('username', 'email', 'role', 'is_active', 'is_staff',)
    search_fields = ('username', 'email')


admin.site.empty_value_display = ADMIN_SITE_EMPTY_VALUE
