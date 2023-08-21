from typing import TYPE_CHECKING, Dict

from rest_framework.utils.serializer_helpers import ReturnDict

from utility.facades import ComponentFacade

if TYPE_CHECKING:
    from channels.models import Channel


class ChannelsFacade(ComponentFacade):

    def summary_serialize_channel(self, channel: 'Channel') -> ReturnDict:
        from channels.views.serializers import ChannelSerializerConfigurer
        return ChannelSerializerConfigurer(mode=ChannelSerializerConfigurer.Mode.SUMMARY).configure(
            instance=channel
        ).data
