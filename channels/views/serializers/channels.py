from collections import OrderedDict
from enum import Enum

from rest_framework import serializers
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
    role = serializers.SerializerMethodField()

    @property
    def ghased(self):
        return self.context['request'].ghased

    def get_role(self, instance: Channel):
        return self.obj_to_role(instance.get_ghased_status_wrt_channel(self.ghased))

    class Role(Enum):
        OWNER = 'owner'
        ADMIN = 'admin'
        SUBSCRIBER = 'subscriber'
        VIEWER = 'viewer'

    def obj_to_role(self, obj):
        if isinstance(obj, ChannelOwner):
            return self.Role.OWNER.value
        if isinstance(obj, ChannelAdmin):
            return self.Role.ADMIN.value
        if isinstance(obj, Subscriber):
            return self.Role.SUBSCRIBER.value
        return self.Role.VIEWER.value

    class Meta(BaseChannelSerializer.Meta):
        fields = [
            *BaseChannelSerializer.Meta.fields,
            'role', 'has_subscription',
        ]


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

    def configure(self, *args, **kwargs):
        return self.configure_class()(*args, **kwargs)
