from django.db import models

from utility.models import CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel


class ChannelContent(CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    channel = models.ForeignKey(
        to='channels.Channel',
        related_name='contents',
        verbose_name='کانال',
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'محتوای کانال'
        verbose_name_plural = 'محتواهای کانال‌ها'
