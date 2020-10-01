from rest_framework import permissions
from core.models import Emprendimiento

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object

        return obj.owner == request.user


class IsParentOwnerOrReadOnly(permissions.BasePermission):

    def has_parent_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        empren = Emprendimiento.Objects.get(owner=request.user.email)
        # Write permissions are allowed only to the owner of the parent object
        return obj.emprendimiento == empren.pk

