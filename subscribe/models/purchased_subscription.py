from django.db import models

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
        status.expires_at += self.subscription.duration
        status.save(update_fields=['expires_at'])

    class Meta:
        verbose_name = 'عضو کانال'
        verbose_name_plural = 'اعضای کانال‌ها'
