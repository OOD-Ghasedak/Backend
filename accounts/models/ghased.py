from typing import Tuple

from django.contrib.auth import get_user_model
from django.db import models

from accounts.models.services.jwt import GhasedJWTHelper
from utility.django import GhasedakMobileNumberValidator
from utility.models import CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel, GhasedakPhoneNumberField


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
