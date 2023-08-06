from typing import TYPE_CHECKING, Type

from financial.models.services.wallet_creation.creator import GhasedWalletCreator
from utility.facades import ComponentFacade

if TYPE_CHECKING:
    from financial.models.services.wallet_creation import WalletCreatorInterface


class FinancialFacade(ComponentFacade):

    def get_wallet_creator_for_ghased_creation(self) -> Type['WalletCreatorInterface']:
        return GhasedWalletCreator
