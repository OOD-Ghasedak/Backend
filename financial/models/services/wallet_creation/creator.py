from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from financial.models import Wallet

if TYPE_CHECKING:
    from accounts.models import Ghased


class WalletCreatorInterface(ABC):
    def __init__(self, ghased: "Ghased"):
        self.__ghased = ghased

    @abstractmethod
    def create(self) -> Wallet:
        pass


class GhasedWalletCreator(WalletCreatorInterface):
    def create(self) -> Wallet:
        return Wallet.objects.create(
            ghased=self.__ghased,
        )
