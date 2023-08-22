from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.models import Ghased
from channel_management.models import ChannelAdmin


class GhasedSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Ghased
        fields = [
            'id',
            'phone_number',
            'email',
            'username',
        ]


class ChannelAdminSerializer(ModelSerializer):
    ghased = GhasedSerializer()

    class Meta:
        model = ChannelAdmin
        fields = [
            'id',
            'channel',
            'share',
            'ghased'
        ]
