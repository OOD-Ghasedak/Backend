from collections import OrderedDict

from rest_framework.serializers import ModelSerializer

from channel_management.models import ChannelManager, ChannelOwner
from channels._ports.serializers import SerializerFacade as ChannelsSerializerFacade


class ManagedChannelsSerializer(ModelSerializer):

    def to_representation(self, instance: ChannelManager):
        return OrderedDict({
            'id': instance.channel.id,
            'manager_id': instance.id,
            'is_owner': isinstance(instance, ChannelOwner),
            **ChannelsSerializerFacade.get_instance().summary_serialize_channel(
                channel=instance.channel
            ),
        })

    class Meta:
        model = ChannelManager
        fields = [
            'id',
        ]
