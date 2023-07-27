from typing import TYPE_CHECKING

from django.db import models

from utility.models import CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel, \
    ConcreteActiveManager

if TYPE_CHECKING:
    from channels.models import Channel


class ChannelManager(CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    concrete_objects = ConcreteActiveManager()

    ghased = models.ForeignKey(
        to='accounts.Ghased',
        related_name='%(class)s',
        verbose_name='قاصد',
        on_delete=models.PROTECT,
    )

    channel: "Channel"

    class Meta:
        verbose_name = 'گرداننده کانال'
        verbose_name_plural = 'گردانندگان کانال'
