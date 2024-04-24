from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import Follow, User


class FollowInline(admin.StackedInline):
    model = Follow
    extra = 0
    fk_name = 'following_author'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following_author', 'created_at',)
    list_editable = ('following_author',)
    list_filter = ('user__username', 'following_author__username')
    search_fields = ('user__username', 'following_author__username')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (FollowInline,)
    list_display = (
        'username',
        'email',
        'is_active',
        'last_login',
        'date_joined',
    )
    list_filter = ('username', 'email', 'is_active', 'is_staff',)
    search_fields = ('username', 'email')


admin.site.empty_value_display = settings.ADMIN_SITE_EMPTY_VALUE
