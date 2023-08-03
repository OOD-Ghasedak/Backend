from enum import Enum

from accounts.models import RegisterOTP
from accounts.models.services.ghased_creation import GhasedCreatorInterface
from accounts.models.services.ghased_creation.required_data import GhasedData
from utility.services import Configurer


class GhasedCreatorConfigurer(Configurer[GhasedCreatorInterface]):
    class Sources(Enum):
        SIGN_UP = 'sign up'
        TEST = 'test'

    def __init__(self, source: Sources):
        self.source = source

    def configure_class(self):
        raise NotImplementedError

    def configure_for_signup(self, username: str, password: str, register_otp: RegisterOTP):
        from accounts.models.services.ghased_creation.creator import SignUpGhasedCreator
        return SignUpGhasedCreator(username, password, register_otp)

    def configure_for_test(self, ghased_data: GhasedData):
        from accounts.models.services.ghased_creation.creator import TestGhasedCreator
        return TestGhasedCreator(ghased_data)

    def configure(self, *args, **kwargs):
        return {
            self.Sources.SIGN_UP: self.configure_for_signup,
            self.Sources.TEST: self.configure_for_test,
        }[self.source](*args, **kwargs)
