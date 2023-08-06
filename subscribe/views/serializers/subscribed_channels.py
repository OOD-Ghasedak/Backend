from collections import OrderedDict

from rest_framework.serializers import ModelSerializer

from channels.facade import ChannelsFacade
from subscribe.models import Subscriber


class SubscribedChannelsSerializer(ModelSerializer):

    def to_representation(self, instance: Subscriber):
        return OrderedDict({
            'id': instance.channel.id,
            'subscriber_id': instance.id,
            'is_premium': instance.subscription_status.is_premium,
            **ChannelsFacade.get_instance().summary_serialize_channel(channel=instance.channel),
        })

    class Meta:
        model = Subscriber
        fields = [
            'id',
        ]
