from typing import TYPE_CHECKING

from django.db import models
from django.db.models import UniqueConstraint, Q
from rest_framework.permissions import BasePermission

from utility.models import CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel, CreationSensitiveModelMixin
from utility.models.managers import filter_active_objects

if TYPE_CHECKING:
    from channels.models import Channel


class IsSubscriberPermission(BasePermission):
    def has_object_permission(self, request, view, obj: 'Channel'):
        return filter_active_objects(obj.subscribers).filter(request.ghased.id).exists()


class Subscriber(CreateHistoryModelMixin, SoftDeleteModelMixin, CreationSensitiveModelMixin, BaseModel):
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

    def after_create(self):
        from subscribe.models import SubscriptionStatus
        SubscriptionStatus.objects.create(subscriber=self)

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('ghased', 'channel'), condition=Q(is_deleted=False), name='unique_subscriber_if_not_deleted'
            ),
        )
        verbose_name = 'عضو کانال'
        verbose_name_plural = 'اعضای کانال‌ها'
