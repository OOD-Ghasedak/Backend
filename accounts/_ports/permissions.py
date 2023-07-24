from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING

from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsGhasedInterface(BasePermission, ABC):
    @abstractmethod
    def has_permission(self, request: Request, view):
        """
        checks whether the `request` is related to a `Ghased`
        attaches the related ghased to the `request` object.
        """


class PermissionsFacade:
    __instance: "PermissionsFacade" = None

    @classmethod
    def get_instance(cls):
        return cls.__instance or cls()

    def get_ghased_permission_class(self) -> Type[IsGhasedInterface]:
        from accounts.views.permissions import IsGhased
        return IsGhased
