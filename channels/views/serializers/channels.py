from collections import OrderedDict
from enum import Enum

from rest_framework.serializers import ModelSerializer

from channel_management.models import ChannelOwner, ChannelAdmin
from channels.models import Channel
from subscribe.models import Subscriber
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


class ChannelGhasedViewSerializer(BaseChannelSerializer):
    def __init__(self, ghased, **kwargs):
        super().__init__(**kwargs)
        self.ghased = ghased

    class Role(Enum):
        OWNER = 'owner'
        ADMIN = 'admin'
        SUBSCRIBER = 'subscriber'
        VIEWER = 'viewer'

    def obj_to_role(self, obj):
        if isinstance(obj, ChannelOwner):
            return ChannelGhasedViewSerializer.Role.OWNER
        if isinstance(obj, ChannelAdmin):
            return ChannelGhasedViewSerializer.Role.ADMIN
        if isinstance(obj, Subscriber):
            return ChannelGhasedViewSerializer.Role.SUBSCRIBER
        return ChannelGhasedViewSerializer.Role.VIEWER

    def to_representation(self, instance: Channel):
        return OrderedDict({
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'role': self.obj_to_role(instance.get_ghased_status_wrt_channel(self.ghased)),
        })


class ChannelSerializerConfigurer(Configurer[BaseChannelSerializer]):
    class Mode(Enum):
        FULL = 'full'
        SUMMARY = 'summary'
        CREATE = 'create'
        GHASED_VIEW = 'ghased_view'

    def __init__(self, mode: Mode):
        self.mode = mode

    def configure_class(self):
        return {
            self.Mode.FULL: ChannelSerializer,
            self.Mode.SUMMARY: ChannelSummarySerializer,
            self.Mode.CREATE: ChannelCreateSerializer,
            self.Mode.GHASED_VIEW: ChannelGhasedViewSerializer,
        }[self.mode]

    def configure(self, channel: Channel):
        return self.configure_class()(instance=channel)
