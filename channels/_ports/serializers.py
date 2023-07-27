from typing import TYPE_CHECKING, Dict

from rest_framework.utils.serializer_helpers import ReturnDict

if TYPE_CHECKING:
    from channels.models import Channel


class SerializerFacade:
    __instance: 'SerializerFacade' = None

    @classmethod
    def get_instance(cls) -> 'SerializerFacade':
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def summary_serialize_channel(self, channel: 'Channel') -> ReturnDict:
        from channels.views.serializers import ChannelSerializerConfigurer
        return ChannelSerializerConfigurer(mode=ChannelSerializerConfigurer.Mode.SUMMARY).configure(channel).data
