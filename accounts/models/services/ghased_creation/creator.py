from abc import ABC, abstractmethod
from typing import Type

from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import Ghased
from accounts.models.services.ghased_creation.required_data import GhasedData
from financial._ports.services import ServicesFacade as FinancialServicesFacade
from financial.models.services.wallet_creation import WalletCreatorInterface


class GhasedCreatorInterface(ABC):
    wallet_creator_class: Type[WalletCreatorInterface]

    @abstractmethod
    def __init__(self, ghased_data: GhasedData):
        pass

    @abstractmethod
    def create(self) -> Ghased:
        pass


class BaseGhasedCreator(GhasedCreatorInterface, ABC):

    def __init__(self, ghased_data: GhasedData):
        self.ghased_data = ghased_data

    def create(self) -> Ghased:
        with transaction.atomic():
            user = self.create_user()
            ghased = self.create_ghased(user)
            self.create_wallet(ghased)
        return ghased

    def create_user(self):
        User = get_user_model()
        user = User.objects.create(
            username=self.ghased_data.username,
            email=self.ghased_data.email,
        )
        user.set_password(self.ghased_data.password)
        user.save()
        return user

    def create_wallet(self, ghased: Ghased):
        return self.wallet_creator_class(ghased).create()

    @abstractmethod
    def create_ghased(self, user):
        pass


class SignUpGhasedCreator(BaseGhasedCreator):
    wallet_creator_class: Type[
        WalletCreatorInterface
    ] = FinancialServicesFacade.get_instance().get_wallet_creator_for_ghased_creation()

    def create_ghased(self, user):
        return Ghased.objects.create(
            user=user,
            phone_number=self.ghased_data.phone_number,
        )
