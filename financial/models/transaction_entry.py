from django.db import models
from django.db.models import F

from utility.models import CreateHistoryModelMixin, CreationSensitiveModelMixin, BaseModel


class TransactionEntry(CreateHistoryModelMixin, CreationSensitiveModelMixin, BaseModel):
    wallet = models.ForeignKey(
        to='financial.Wallet',
        related_name='entries',
        verbose_name='کیف‌ پول',
        on_delete=models.PROTECT,
    )
    transaction = models.ForeignKey(
        to='financial.Transaction',
        related_name='entries',
        verbose_name='تراکنش مربوطه',
        on_delete=models.PROTECT,
        null=True, blank=True,
    )
    amount = models.PositiveBigIntegerField(verbose_name='مقدار')

    def after_create(self):
        self.wallet.__class__.objects.update(balance=F('balance') + self.amount)

    class Meta:
        verbose_name = 'ورودی کیف‌ پول'
        verbose_name_plural = 'ورودی‌های کیف‌ پول'
