from django.db import models
from django.utils import timezone

from utility.models import BaseModel, CreateHistoryModelMixin, CreationSensitiveModelMixin


class PurchasedSubscription(CreateHistoryModelMixin, CreationSensitiveModelMixin, BaseModel):
    subscription = models.ForeignKey(
        to='channels.Subscription',
        related_name='purchased_subscriptions',
        on_delete=models.PROTECT,
        verbose_name='اشتراک',
    )

    subscriber = models.ForeignKey(
        to='subscribe.Subscriber',
        related_name='purchased_subscriptions',
        on_delete=models.PROTECT,
        verbose_name='عضو کانال',
    )

    def after_create(self):
        status = self.subscriber.subscription_status
        if status.is_premium:
            status.expires_at += self.subscription.duration
        else:
            status.expires_at = timezone.now() + self.subscription.duration
        status.save(update_fields=['expires_at'])

    class Meta:
        verbose_name = 'عضو کانال'
        verbose_name_plural = 'اعضای کانال‌ها'
