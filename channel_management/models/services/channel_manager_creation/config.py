from enum import Enum

from utility.services import Configurer
from channel_management.models.services.channel_manager_creation import ChannelManagerCreatorInterface
from channel_management.models.services.channel_manager_creation.required_data import ManagerData


class ChannelManagerCreatorConfigurer(Configurer[ChannelManagerCreatorInterface]):
    class Sources(Enum):
        OWNER = 'owner'
        ADMIN = 'admin'

    def __init__(self, source: Sources):
        self.source = source

    def configure_class(self):
        raise NotImplementedError

    def configure_for_owner(self, manager_data: ManagerData):
        from channel_management.models.services.channel_manager_creation.creator import ChannelOwnerCreator
        return ChannelOwnerCreator(manager_data)

    def configure_for_admin(self, manager_data: ManagerData):
        from channel_management.models.services.channel_manager_creation.creator import ChannelAdminCreator
        return ChannelAdminCreator(manager_data)

    def configure(self, manager_data: ManagerData) -> ChannelManagerCreatorInterface:
        return {
            self.Sources.OWNER: self.configure_for_owner(manager_data),
            self.Sources.ADMIN: self.configure_for_admin(manager_data),
        }[self.source]
