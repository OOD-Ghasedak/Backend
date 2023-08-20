from django.db import models
from django.utils import timezone

from utility.models import CreateHistoryModelMixin, UpdateHistoryModelMixin, BaseModel


class SubscriptionStatus(CreateHistoryModelMixin, UpdateHistoryModelMixin, BaseModel):
    expires_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ انقضا',
        null=True, blank=True,
    )

    subscriber = models.OneToOneField(
        to='subscribe.Subscriber',
        related_name='subscription_status',
        on_delete=models.CASCADE,
        verbose_name='عضو کانال',
    )

    @property
    def is_premium(self):
        return bool(self.expires_at) and self.expires_at > timezone.now()
