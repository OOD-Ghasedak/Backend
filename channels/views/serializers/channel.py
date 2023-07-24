from enum import Enum

from rest_framework.serializers import ModelSerializer

from channels.models import Channel
from utility.services import Configurer


class BaseChannelSerializer(ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'id',
            'name',
            'description'
        ]


class ChannelSummarySerializer(BaseChannelSerializer):
    pass


class ChannelSerializer(BaseChannelSerializer):
    pass


class ChannelCreateSerializer(BaseChannelSerializer):
    pass


class ChannelSerializerConfigurer(Configurer[BaseChannelSerializer]):
    class Mode(Enum):
        FULL = 'full'
        SUMMARY = 'summary'
        CREATE = 'create'

    def __init__(self, mode: Mode):
        self.mode = mode

    def configure_class(self):
        return {
            self.Mode.FULL: ChannelSerializer,
            self.Mode.SUMMARY: ChannelSummarySerializer,
            self.Mode.CREATE: ChannelCreateSerializer,
        }[self.mode]

    def configure(self, channel: Channel):
        return self.configure_class()(instance=channel)
