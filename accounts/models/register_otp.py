from typing import Optional

from django.db import models, transaction
from django.db.models import Exists, Q, OuterRef, CheckConstraint
from django.utils import timezone

from accounts.models import OTP, EMAIL_AND_PHONE_NUMBER_NOT_BOTH_NULL
from utility.models import GhasedakPhoneNumberField, BaseModel


class RegisterOTP(BaseModel):
    REGISTER_OTP_LENGTH = 4
    REGISTER_OTP_AVAILABLE_KEYS = '0123456789'
    REGISTER_OTP_DURATION = timezone.timedelta(minutes=2)

    otp = models.OneToOneField(
        to='accounts.OTP',
        on_delete=models.PROTECT,
        related_name='register_otp',
        verbose_name='کد احراز',
    )

    email = models.EmailField(null=True, blank=True)
    phone_number = GhasedakPhoneNumberField(null=True, blank=True)

    @property
    def code(self):
        return self.otp.code

    @classmethod
    def _get_valid_register_otp_filter(cls, otp_code: str) -> Q:
        return Q(
            otp__code=otp_code,
            otp__is_valid=True,
            otp__created__gt=timezone.now() - cls.REGISTER_OTP_DURATION,
        )

    @classmethod
    def generate_register_otp(cls, email: Optional[str], phone_number: Optional[str]) -> 'RegisterOTP':
        with transaction.atomic():
            OTP.objects.annotate(
                has_previous_otp=Exists(
                    RegisterOTP.objects.filter(
                        Q(email=email) | Q(phone_number=phone_number),
                        otp=OuterRef('id'),
                    )
                )
            ).filter(
                is_valid=True,
                has_previous_otp=True,
            ).update(is_valid=False)
            while True:
                otp = OTP.generate_otp(cls.REGISTER_OTP_LENGTH, cls.REGISTER_OTP_AVAILABLE_KEYS, save=False)
                if not RegisterOTP.objects.filter(
                    cls._get_valid_register_otp_filter(otp.code)
                ).exists():
                    break
            return cls.objects.create(
                otp=OTP.generate_otp(cls.REGISTER_OTP_LENGTH, cls.REGISTER_OTP_AVAILABLE_KEYS),
                email=email,
                phone_number=phone_number,
            )

    @classmethod
    def get_from_otp_code(cls, otp_code: str) -> 'RegisterOTP':
        return cls.objects.get(
            cls._get_valid_register_otp_filter(otp_code),
        )

    def mark_as_used(self):
        self.otp.is_valid = False
        self.otp.save(update_fields=['is_valid'])

    class Meta:
        constraints = (
            CheckConstraint(
                check=EMAIL_AND_PHONE_NUMBER_NOT_BOTH_NULL,
                name='email_and_phone_number_not_both_null_in_otp'
            ),
        )
        # TODO: add verbose
