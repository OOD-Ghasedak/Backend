from enum import Enum
from typing import Type

from accounts.models.services.ghased_creation import GhasedCreatorInterface
from accounts.models.services.ghased_creation.required_data import GhasedData
from financial.models.services.wallet_creation import WalletCreatorConfigurer
from utility.services import Configurer, T


class GhasedCreatorConfigurer(Configurer[GhasedCreatorInterface]):
    class Sources(Enum):
        SIGN_UP = 'sign up'

    def __init__(self, source: Sources):
        self.source = source

    def configure_class(self) -> Type[T]:
        raise NotImplementedError

    def configure(self, ghased_data: GhasedData):
        from accounts.models.services.ghased_creation.creator import SignUpGhasedCreator
        wallet_creator_class = WalletCreatorConfigurer(
            WalletCreatorConfigurer.Sources.GHASED_CREATION
        ).configure_class()
        return {
            self.Sources.SIGN_UP: SignUpGhasedCreator,
        }[self.source](ghased_data, wallet_creator_class)
