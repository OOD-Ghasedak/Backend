from django.db import models
from django.db.models import UniqueConstraint, Q
from django.utils import timezone

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
                (cls.THREE_MONTH, cls.THREE_MONTH_FA),
                (cls.SIX_MONTH, cls.SIX_MONTH_FA),
                (cls.TWELVE_MONTH, cls.TWELVE_MONTH_FA),
            )

    duration_choice = models.CharField(
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

    price = models.PositiveBigIntegerField(
        verbose_name='قیمت اشتراک',
    )

    @property
    def duration(self):
        return {
            self.DurationChoices.ONE_MONTH: timezone.timedelta(days=30),
            self.DurationChoices.THREE_MONTH: timezone.timedelta(days=3 * 30),
            self.DurationChoices.SIX_MONTH: timezone.timedelta(days=6 * 30),
            self.DurationChoices.TWELVE_MONTH: timezone.timedelta(days=12 * 30),
        }[self.duration_choice]

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('channel', 'duration_choice'), condition=Q(is_deleted=False),
                name='unique_duration_for_channel',
            ),
        )
        verbose_name = 'اشتراک'
        verbose_name_plural = 'اشتراک‌های کانال‌ها'
