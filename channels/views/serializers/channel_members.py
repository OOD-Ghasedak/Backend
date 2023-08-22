from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.models import Ghased
from channel_management.models import ChannelAdmin
from subscribe.models import Subscriber


class GhasedSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username')
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, instance: Ghased):
        return instance.user.get_full_name()

    class Meta:
        model = Ghased
        fields = [
            'id',
            'phone_number',
            'email',
            'username',
            'full_name'
        ]


class ChannelAdminSerializer(ModelSerializer):
    ghased = GhasedSerializer()

    class Meta:
        model = ChannelAdmin
        fields = [
            'id',
            'channel',
            'share',
            'ghased',
        ]


class SubscriberSerializer(ModelSerializer):
    ghased = GhasedSerializer()

    class Meta:
        model = Subscriber
        fields = [
            'id',
            'channel',
            'ghased',
        ]
