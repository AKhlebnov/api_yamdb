from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Разрешает доступ только админу.
    """
    message = 'Доступно только админу.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsSuperuser(permissions.BasePermission):
    """
    Разрешает доступ только суперпользователю.
    """
    message = 'Доступно только суперюзеру.'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_superuser)


class IsModerator(permissions.BasePermission):
    """
    Разрешает доступ только модерутору.
    """
    message = 'Доступно только модератору.'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == 'moderator')


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только админу, остальным чтение.
    """
    message = 'Изменить контент может только админ.'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == 'admin'))


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только автору объекта, остальным чтение.
    """
    message = 'Изменить контент может только автор.'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and obj.user == request.user))


class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только модераторам, остальным чтение.
    """
    message = 'Изменить контент может только модератор.'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == 'moderator'))


class IsSuperuserOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только суперпользователю Django, остальным чтение.
    """
    message = 'Изменить контент может только суперпользователь.'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_superuser))
