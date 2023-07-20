from utility.models import CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel


class Channel(CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):

    class Meta:
        verbose_name = 'کانال'
        verbose_name_plural = 'کانال‌ها'
