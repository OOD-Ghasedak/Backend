from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.models import Ghased
from channels.models import ChannelContent, ContentFile, Channel
from subscribe.models import Subscriber
from utility.services import Configurer


class ChannelContentSerializer(ModelSerializer):
    class Meta:
        model = ChannelContent


class FreeContentSerializer(ChannelContentSerializer):
    class Meta(ChannelContentSerializer.Meta):
        fields = [
            'title', 'summary', 'is_perimum',
        ]


class ContentFileSerializer(ModelSerializer):
    class Meta:
        model = ContentFile
        fields = [
            'file',
            'file_type',
        ]


class FullFeatureContentSerializer(ChannelContentSerializer):
    file = serializers.SerializerMethodField()

    def get_content_file(self, instance: ChannelContent):
        return ContentFileSerializer(
            instance.files.first(),
            allow_null=True,
            context=self.context,
        ).data

    class Meta(ChannelContentSerializer.Meta):
        fields = [
            'title', 'summary', 'is_perimum', 'text', 'file',
        ]


class ChannelContentSerializerConfigurer(Configurer[ChannelContentSerializer]):

    def __init__(self, ghased: Ghased, channel_id: int):
        self.ghased = ghased
        self.channel = Channel.objects.get(id=channel_id)

    def configure_class(self):
        status = self.channel.get_ghased_status_wrt_channel(self.ghased)
        if status is None or (isinstance(status, Subscriber) and not status.subscription_status.is_premium):
            return FreeContentSerializer
        return FullFeatureContentSerializer

    def configure(self, *args, **kwargs):
        return self.configure_class()(*args, **kwargs)
