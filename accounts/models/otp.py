import random

from django.db import models

from utility.models import CreateHistoryModelMixin, BaseModel


class OTP(CreateHistoryModelMixin, BaseModel):
    code = models.CharField(
        max_length=256,
        verbose_name='کد OTP',
    )

    is_valid = models.BooleanField(
        default=True,
        verbose_name='معتبر است',
        db_index=True,
    )

    @classmethod
    def generate_otp(cls, otp_length: int, available_keys: str, *, save=True):
        otp: 'OTP' = cls(code=''.join(random.choices(available_keys, k=otp_length)))
        if save:
            otp.save()
        return otp

    # TODO: class Meta
