from typing import TYPE_CHECKING

from django.db import models
from rest_framework.permissions import BasePermission

from channel_management.models import ChannelManager

if TYPE_CHECKING:
    from channels.models import Channel


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj: Channel):
        return obj.owner.ghased_id == request.ghased.id


class ChannelOwner(ChannelManager):
    channel = models.OneToOneField(
        to='channels.Channel',
        related_name='owner',
        on_delete=models.PROTECT,
        verbose_name='کانال'
    )

    class Meta:
        verbose_name = 'مالک کانال'
        verbose_name_plural = 'مالکین کانال‌ها'
