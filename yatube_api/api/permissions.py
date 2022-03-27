from rest_framework.permissions import BasePermission, SAFE_METHODS


class OnlyAuthorChangeContent(BasePermission):
    message = 'Только автор может изменить контент.'

    def has_object_permission(self, request, view, obj):
        permission = (
            request.user == obj.author or request.method in SAFE_METHODS
        )
        return permission
