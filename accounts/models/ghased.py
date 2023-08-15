from typing import Tuple

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, CheckConstraint
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


EMAIL_AND_PHONE_NUMBER_NOT_BOTH_NULL = Q(
    Q(Q(email__isnull=False) & ~Q(email='')) |
    Q(Q(phone_number__isnull=False) & ~Q(phone_number=''))
)


class Ghased(CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    user = models.OneToOneField(
        to=get_user_model(),
        related_name='ghased',
        on_delete=models.PROTECT,
        verbose_name='کاربر جنگو'
    )

    email = models.EmailField(verbose_name='ایمیل کاربر', blank=True, null=True, unique=True)

    phone_number = GhasedakPhoneNumberField(
        unique=True, blank=True, null=True,
    )

    def get_jwt_tokens(self) -> Tuple[str, str]:
        return GhasedJWTHelper(self).get_jwt_tokens()

    class Meta:
        verbose_name = 'قاصد'
        verbose_name_plural = 'قاصدها'
        constraints = (
            CheckConstraint(
                check=EMAIL_AND_PHONE_NUMBER_NOT_BOTH_NULL,
                name='email_and_phone_number_not_both_null_in_ghased'
            ),
        )
