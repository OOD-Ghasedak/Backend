from typing import TYPE_CHECKING

from django.db import models
from rest_framework.permissions import BasePermission

from channel_management.models import ChannelManager
from utility.models import PercentageField

if TYPE_CHECKING:
    from channels.models import Channel


class IsAdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj: 'Channel'):
        return obj.admins.filter(ghased_id=request.ghased.id).exists()


class ChannelAdmin(ChannelManager):
    channel = models.ForeignKey(
        to='channels.Channel',
        related_name='admins',
        on_delete=models.PROTECT,
        verbose_name='کانال',
    )

    share = PercentageField(
        verbose_name='درصد سهم',
        null=True, blank=True,
    )

    class Meta:
        verbose_name = 'مالک کانال'
        verbose_name_plural = 'مالکین کانال‌ها'
