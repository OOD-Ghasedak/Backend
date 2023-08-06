from typing import Tuple

from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.permissions import BasePermission

from accounts.models.services.jwt import GhasedJWTHelper
from utility.models import CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel, GhasedakPhoneNumberField


class IsGhasedPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            ghased = request.user.ghased
            setattr(request, 'ghased', ghased)
            return request
        except:
            return False


class Ghased(CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    user = models.OneToOneField(
        to=get_user_model(),
        related_name='ghased',
        on_delete=models.PROTECT,
        verbose_name='کاربر جنگو'
    )

    phone_number = GhasedakPhoneNumberField(
        unique=True,
    )

    def get_jwt_tokens(self) -> Tuple[str, str]:
        return GhasedJWTHelper(self).get_jwt_tokens()

    class Meta:
        verbose_name = 'قاصد'
        verbose_name_plural = 'قاصدها'
