from enum import Enum

from accounts.models.services.ghased_creation import GhasedCreatorInterface
from accounts.models.services.ghased_creation.required_data import GhasedData
from utility.services import Configurer


class GhasedCreatorConfigurer(Configurer[GhasedCreatorInterface]):
    class Sources(Enum):
        SIGN_UP = 'sign up'

    def __init__(self, source: Sources):
        self.source = source

    def configure_class(self):
        raise NotImplementedError

    def configure(self, ghased_data: GhasedData):
        from accounts.models.services.ghased_creation.creator import SignUpGhasedCreator
        return {
            self.Sources.SIGN_UP: SignUpGhasedCreator,
        }[self.source](ghased_data)
