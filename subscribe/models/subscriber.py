from django.db import models
from django.db.models import UniqueConstraint, Q

from utility.models import CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel


class Subscriber(CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):

    channel = models.ForeignKey(
        to='channels.Channel',
        related_name='subscribers',
        verbose_name='کانال',
        on_delete=models.PROTECT,
    )

    ghased = models.ForeignKey(
        to='accounts.Ghased',
        related_name='subscribers',
        verbose_name='قاصد',
        on_delete=models.PROTECT,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('ghased', 'channel'), condition=Q(is_deleted=False), name='unique_subscriber_if_not_deleted'
            ),
        )
        verbose_name = 'عضو کانال'
        verbose_name_plural = 'اعضای کانال‌ها'
