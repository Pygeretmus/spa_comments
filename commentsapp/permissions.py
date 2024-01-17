from django.http import Http404
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrAuthenticatedOrPost(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(request.method == "POST" or (request.user and request.user.is_authenticated))

    def has_object_permission(self, request, view, obj):
        return bool(request.user and (request.method in SAFE_METHODS or obj.id == request.user.id))


class IsOwnerOrAuthenticated(BasePermission):
    """
    The request is authenticated as a comment owner, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and (request.method in SAFE_METHODS or obj.user == request.user))
