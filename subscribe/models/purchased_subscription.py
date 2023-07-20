from django.db import models
from django.db.models import UniqueConstraint, Q

from utility.models import BaseModel, CreateHistoryModelMixin, SoftDeleteModelMixin


class PurchasedSubscription(CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    subscription = models.ForeignKey(
        to='channels.subscription',
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

    expires_at = models.DateTimeField(
        verbose_name='زمان انقضا',
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('subscriber', 'subscription'), condition=Q(is_deleted=False),
                name='unique_purchased_subscription_if_not_deleted',
            ),
        )
        verbose_name = 'عضو کانال'
        verbose_name_plural = 'اعضای کانال‌ها'
