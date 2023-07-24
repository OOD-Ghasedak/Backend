from rest_framework.permissions import BasePermission

from channels.models import Channel


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj: Channel):
        return obj.owner.ghased_id == request.ghased.id


class IsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj: Channel):
        return obj.admins.filter(ghased_id=request.ghased.id).exists()


IsManager = IsOwner | IsAdmin
