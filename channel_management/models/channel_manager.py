from typing import TYPE_CHECKING

from django.db import models

from utility.models import CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel

if TYPE_CHECKING:
    from channels.models import Channel


class ChannelManager(CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    ghased = models.ForeignKey(
        to='accounts.Ghased',
        related_name='%(class)s',
        verbose_name='قاصد',
        on_delete=models.PROTECT,
    )

    channel: "Channel"

    class Meta:
        abstract = True
        verbose_name = 'گرداننده کانال'
        verbose_name_plural = 'گردانندگان کانال'
