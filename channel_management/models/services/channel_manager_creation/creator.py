from abc import ABC, abstractmethod

from channel_management.models import ChannelManager, ChannelAdmin, ChannelOwner
from channel_management.models.services.channel_manager_creation.required_data import ManagerData


class ChannelManagerCreatorInterface(ABC):
    def __init__(self, manager_data):
        self.manager_data = manager_data

    @abstractmethod
    def create(self) -> ChannelManager:
        ...


class ChannelAdminCreator(ChannelManagerCreatorInterface):
    def __init__(self, manager_data):
        super().__init__(manager_data)

    def create(self) -> ChannelAdmin:
        return ChannelAdmin.objects.create(ghased=self.manager_data.ghased, channel=self.manager_data.channel)


class ChannelOwnerCreator(ChannelManagerCreatorInterface):
    def __init__(self, manager_data):
        super().__init__(manager_data)

    def create(self) -> ChannelOwner:
        return ChannelOwner.objects.create(ghased=self.manager_data.ghased, channel=self.manager_data.channel)
