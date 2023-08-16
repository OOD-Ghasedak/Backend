from django.db import models
from django.db.models import UniqueConstraint, Q
from django.utils import timezone

from utility.django import Choices
from utility.models import CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel


class Subscription(CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    class DurationChoices(Choices):
        ONE_MONTH = Choices.Choice('one month', 'یک ماهه')
        THREE_MONTH = Choices.Choice('three month', 'سه ماهه')
        SIX_MONTH = Choices.Choice('six month', 'شش ماهه')
        TWELVE_MONTH = Choices.Choice('twelve month', 'دوازده ماهه')

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
