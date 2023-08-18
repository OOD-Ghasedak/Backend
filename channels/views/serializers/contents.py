from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.models import Ghased
from channels.models import ChannelContent, ContentFile, Channel
from subscribe.models import Subscriber
from utility.api_file_handling import ConfiguredSecuredFileSerializerMeta
from utility.services import Configurer


class ChannelContentSerializer(ModelSerializer):
    class Meta:
        model = ChannelContent


class FreeContentSerializer(ChannelContentSerializer):
    class Meta(ChannelContentSerializer.Meta):
        fields = [
            'title', 'summary', 'is_perimum', 'price',
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
            'title', 'summary', 'is_perimum', 'price', 'text', 'file',
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


class CreateContentFileSerializer(ModelSerializer, metaclass=ConfiguredSecuredFileSerializerMeta):
    securing_file_fields = ['file']
    accepted_mime_types = settings.ACCEPTED_MIME_TYPES['content_file']
    file_size_limit = settings.ACCEPTED_FILE_SIZES['content_file'] * (1 << 20)

    class Meta:
        model = ContentFile
        fields = [
            'id',
            'file',
            'file_type',
        ]


class CreateUpdateChannelContnentSerializer(ModelSerializer):
    files = CreateContentFileSerializer(required=False)

    def create(self, validated_data):
        with transaction.atomic():
            files = validated_data.pop('files', None)
            channel_content: ChannelContent = super().create(validated_data)
            for datum in files:
                serializer = CreateContentFileSerializer(data=datum, context=self.context)
                serializer.is_valid(raise_exception=True)
                serializer.save(content=channel_content)
            return channel_content

    def update(self, instance, validated_data):
        with transaction.atomic():
            validated_data.pop('files', None)
            channel_content: ChannelContent = super().update(instance, validated_data)
            return channel_content

    class Meta:
        model = ChannelContent
        fields = [
            'title', 'summary', 'price', 'text', 'files',
        ]
