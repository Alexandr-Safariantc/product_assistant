from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrAdminOrSuperuser(BasePermission):
    """Allow non-safe methods for author, admin, superuser."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin
                 or request.user == obj.author)
        )
