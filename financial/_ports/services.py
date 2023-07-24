from typing import TYPE_CHECKING, Type

from financial.models.services.wallet_creation.creator import GhasedWalletCreator

if TYPE_CHECKING:
    from financial.models.services.wallet_creation import WalletCreatorInterface


class ServicesFacade:
    __instance: 'ServicesFacade' = None

    @classmethod
    def get_instance(cls) -> 'ServicesFacade':
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def get_wallet_creator_for_ghased_creation(self) -> Type['WalletCreatorInterface']:
        return GhasedWalletCreator
