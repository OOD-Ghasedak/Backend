from django.contrib.auth import get_user_model
from django.db import models

from accounts.jwt import JWTClaimsHelper
from utility.django import GhasedakMobileNumberValidator
from utility.models import CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel


class Ghased(CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    user = models.OneToOneField(
        to=get_user_model(),
        related_name='ghased',
        on_delete=models.PROTECT,
        verbose_name='کاربر جنگو'
    )

    phone_number = models.CharField(
        max_length=13,
        verbose_name='شماره همراه',
        unique=True,
        validators=[GhasedakMobileNumberValidator()]
    )

    @property
    def jwt_claims_helper(self) -> JWTClaimsHelper:
        return JWTClaimsHelper(
            self,
            [
                ('id', 'ghased_id'),
                ('user.id', 'user_id'),
                'phone_number',
            ]
        )

    class Meta:
        verbose_name = 'قاصد'
        verbose_name_plural = 'قاصدها'
