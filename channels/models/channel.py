from django.db import models

from utility.models import CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel


class Channel(CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    name = models.CharField(
        unique=True,
        verbose_name='نام',
        max_length=256
    )

    description = models.TextField(verbose_name='بیوگرافی کانال')

    class Meta:
        verbose_name = 'کانال'
        verbose_name_plural = 'کانال‌ها'
