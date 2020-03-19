from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsSameUserAsAuthenticated(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj == request.user)


class IsObjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.owner == request.user)


class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(isinstance(request.user, AnonymousUser))
