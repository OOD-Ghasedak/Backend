from enum import Enum

from financial.models.services.wallet_creation import WalletCreatorInterface
from financial.models.services.wallet_creation.creator import GhasedCreationWalletCreator
from utility.services import Configurer, T


class WalletCreatorConfigurer(Configurer[WalletCreatorInterface]):
    class Sources(Enum):
        GHASED_CREATION = 'ghased creation'

    def __init__(self, source: Sources):
        self.source = source

    def configure_class(self):
        return {
            self.Sources.GHASED_CREATION: GhasedCreationWalletCreator,
        }[self.source]

    def configure(self, *args, **kwargs) -> T:
        raise NotImplementedError
