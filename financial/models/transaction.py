from utility.models import CreateHistoryModelMixin, BaseModel


class Transaction(CreateHistoryModelMixin, BaseModel):
    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش‌ها'
