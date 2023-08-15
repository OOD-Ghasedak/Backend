from abc import ABC, abstractmethod
from typing import Type

from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import Ghased, RegisterOTP
from accounts.models.services.ghased_creation.required_data import GhasedData
from financial.facade import FinancialFacade
from financial.models.services.wallet_creation import WalletCreatorInterface


class GhasedCreatorInterface(ABC):
    wallet_creator_class: Type[WalletCreatorInterface]

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
            email='ghased@ghasedak.org',
        )
        user.set_password(self.ghased_data.password)
        user.save()
        return user

    def create_wallet(self, ghased: Ghased):
        return self.wallet_creator_class(ghased).create()

    def create_ghased(self, user):
        return Ghased.objects.create(
            user=user,
            phone_number=self.ghased_data.phone_number,
            email=self.ghased_data.email,
        )


class SignUpGhasedCreator(BaseGhasedCreator):
    wallet_creator_class: Type[
        WalletCreatorInterface
    ] = FinancialFacade.get_instance().get_wallet_creator_for_ghased_creation()

    def __init__(self, username, password, register_otp: RegisterOTP):
        self._register_otp = register_otp
        super().__init__(GhasedData(
            username=username,
            password=password,
            email=register_otp.email,
            phone_number=register_otp.phone_number,
        ))

    def create(self) -> Ghased:
        ghased = super(SignUpGhasedCreator, self).create()
        self._register_otp.mark_as_used()
        return ghased


class TestGhasedCreator(BaseGhasedCreator):
    wallet_creator_class: Type[
        WalletCreatorInterface
    ] = FinancialFacade.get_instance().get_wallet_creator_for_ghased_creation()
