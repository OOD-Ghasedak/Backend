from typing import TYPE_CHECKING, Type

from financial.models import Wallet, Transaction, TransactionEntry
from financial.models.services.wallet_creation.creator import GhasedWalletCreator
from utility.facades import ComponentFacade

if TYPE_CHECKING:
    from financial.models.services.wallet_creation import WalletCreatorInterface


class FinancialFacade(ComponentFacade):

    def get_wallet_creator_for_ghased_creation(self) -> Type['WalletCreatorInterface']:
        return GhasedWalletCreator

    def transact(self, source: Wallet, dist: Wallet, amount):
        tr = Transaction.objects.create()
        source_tr_entry = TransactionEntry.objects.create(transaction=tr, amount=-amount, wallet=source)
        dist_tr_entry = TransactionEntry.objects.create(transaction=tr, amount=amount, wallet=dist)
