from typing import TYPE_CHECKING, List

from django.db import transaction

from utility.models import CreateHistoryModelMixin, BaseModel

if TYPE_CHECKING:
    from financial.models import Wallet


class Transaction(CreateHistoryModelMixin, BaseModel):
    @classmethod
    def pay(cls, payer_wallet: 'Wallet', payee_wallet: 'Wallet', amount: int) -> 'Transaction':
        assert amount > 0
        with transaction.atomic():
            tr = Transaction.objects.create()
            from financial.models import TransactionEntry
            TransactionEntry.objects.create(
                wallet=payer_wallet,
                amount=-amount,
                transaction=tr,
            )
            TransactionEntry.objects.create(
                wallet=payee_wallet,
                amount=+amount,
                transaction=tr,
            )
        return tr

    @classmethod
    def multi_pay(cls, payer_wallet: 'Wallet', payee_wallets: List['Wallet'], amounts: List[int]):
        assert all(list(map(lambda amount: amount > 0, amounts)))
        with transaction.atomic():
            tr = Transaction.objects.create()
            from financial.models import TransactionEntry
            sum_amounts = sum(amounts)
            TransactionEntry.objects.create(
                wallet=payer_wallet,
                amount=-sum_amounts,
                transaction=tr,
            )
            for i, payee_wallet in payee_wallets:
                amount = amounts[i]
                TransactionEntry.objects.create(
                    wallet=payee_wallet,
                    amount=+amount,
                    transaction=tr,
                )
        return tr

    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش‌ها'
