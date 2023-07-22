from django.db import models

from utility.models import CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel


class Subscription(CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    class DurationChoices:
        ONE_MONTH = 'one month'
        ONE_MONTH_FA = 'یک ماهه'
        THREE_MONTH = 'three month'
        THREE_MONTH_FA = 'سه ماهه'
        SIX_MONTH = 'six month'
        SIX_MONTH_FA = 'شش ماهه'
        TWELVE_MONTH = 'twelve month'
        TWELVE_MONTH_FA = 'دوازده ماهه'

        @classmethod
        def get_choices(cls):
            return (
                (cls.ONE_MONTH, cls.ONE_MONTH_FA),
                (cls.THREE_MONTH, cls.THREE_MONTH),
                (cls.SIX_MONTH, cls.SIX_MONTH),
                (cls.TWELVE_MONTH, cls.TWELVE_MONTH_FA),
            )

    duration = models.CharField(
        max_length=128,
        choices=DurationChoices.get_choices(),
        verbose_name='دوره',
    )

    channel = models.ForeignKey(
        to='channels.Channel',
        related_name='subscriptions',
        verbose_name='کانال',
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'اشتراک'
        verbose_name_plural = 'اشتراک‌های کانال‌ها'