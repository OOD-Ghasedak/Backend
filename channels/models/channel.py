from typing import Union, Optional

from django.db import models

from channel_management.models import ChannelOwner, ChannelAdmin
from subscribe.models import Subscriber
from utility.models import CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel


class Channel(CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    name = models.CharField(
        unique=True,
        verbose_name='نام',
        max_length=256
    )

    description = models.TextField(verbose_name='بیوگرافی کانال')

    def get_ghased_status_wrt_channel(self, ghased) -> Optional[Union[ChannelOwner, ChannelAdmin, Subscriber]]:
        if self.owner.ghased_id == ghased.id:
            return self.owner
        if found_admin := self.admins.filter(ghased_id=ghased.id).first():
            return found_admin
        if found_subscriber := self.subscribers.filter(ghased_id=ghased.id).first():
            return found_subscriber
        return None


    class Meta:
        verbose_name = 'کانال'
        verbose_name_plural = 'کانال‌ها'
