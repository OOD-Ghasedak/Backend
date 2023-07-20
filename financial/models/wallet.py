from django.db import models

from utility.models import CreateHistoryModelMixin, UpdateHistoryModelMixin, BaseModel


class Wallet(CreateHistoryModelMixin, UpdateHistoryModelMixin, BaseModel):
    ghased = models.OneToOneField(
        to='accounts.Ghased',
        related_name='wallet',
        on_delete=models.PROTECT,
        verbose_name='قاصد'
    )

    balance = models.PositiveBigIntegerField(
        verbose_name='موجودی',
    )

    class Meta:
        verbose_name = 'کیف پول'
        verbose_name_plural = 'کیف پول‌ها'
