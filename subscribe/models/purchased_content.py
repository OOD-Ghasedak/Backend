from django.db import models

from utility.models import BaseModel, CreateHistoryModelMixin


class PurchasedContent(CreateHistoryModelMixin, BaseModel):
    content = models.ForeignKey(
        to='channels.ChannelContent',
        related_name='purchased_contents',
        on_delete=models.PROTECT,
        verbose_name='محتوا',
    )

    subscriber = models.ForeignKey(
        to='subscribe.Subscriber',
        related_name='purchased_contents',
        on_delete=models.PROTECT,
        verbose_name='عضو کانال',
    )

    class Meta:
        verbose_name = 'محتوای خریداری شده'
        verbose_name_plural = 'محتواهای خریداری شده'
