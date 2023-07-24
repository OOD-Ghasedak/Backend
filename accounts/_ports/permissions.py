from abc import abstractmethod
from typing import Type

from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsGhasedInterface(BasePermission):
    @abstractmethod
    def has_permission(self, request: Request, view):
        """
        checks whether the `request` is related to a `Ghased`
        attaches the related ghased to the `request` object.
        """


class PermissionsFacade:
    __instance: 'PermissionsFacade' = None

    @classmethod
    def get_instance(cls) -> 'PermissionsFacade':
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def get_ghased_permission_class(self) -> Type[IsGhasedInterface]:
        from accounts.views.permissions import IsGhased
        return IsGhased
