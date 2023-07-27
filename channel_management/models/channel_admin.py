from django.db import models

from channel_management.models import ChannelManager


class ChannelAdmin(ChannelManager):
    channel = models.ForeignKey(
        to='channels.Channel',
        related_name='admins',
        on_delete=models.PROTECT,
        verbose_name='کانال'
    )

    class Meta:
        verbose_name = 'مالک کانال'
        verbose_name_plural = 'مالکین کانال‌ها'
