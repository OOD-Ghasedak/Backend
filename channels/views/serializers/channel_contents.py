from django.conf import settings
from django.core.files import File
from django.db import transaction
from django.db.models import Manager
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ListSerializer

from accounts.models import Ghased
from channels.models import ChannelContent, ContentFile, Channel
from subscribe.models import Subscriber
from utility.api_file_handling import ConfiguredSecuredFileSerializerMeta
from utility.services import Configurer


class ChannelContentsListSerializer(ListSerializer):

    def update(self, instance, validated_data):
        raise NotImplementedError

    @property
    def status(self):
        return self.context['status']

    def get_child_for_content(self, content: ChannelContent):
        if content.is_premium and (
                self.status is None
                or (
                        isinstance(self.status, Subscriber)
                        and not self.status.subscription_status.is_premium
                        and not self.status.purchased_contents.filter(content_id=content.id).exists()
                )
        ):
            return FreeContentSerializer
        return FullFeatureContentSerializer

    def to_representation(self, data):
        iterable = data.all() if isinstance(data, Manager) else data
        result = []
        for item in iterable:
            child = self.get_child_for_content(item)(item, context=self.context)
            result.append(child.data)
        return result


class ChannelContentSerializer(ModelSerializer):
    complete_content = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()

    def get_content_type(self, instance: ChannelContent):
        try:
            return instance.file.file_type
        except AttributeError:
            return 'text'

    class Meta:
        model = ChannelContent
        fields = [
            'id',
            'content_type',
            'complete_content',
        ]
        list_serializer_class = ChannelContentsListSerializer


class FreeContentSerializer(ChannelContentSerializer):

    def get_complete_content(self, instance: ChannelContent):
        return None

    class Meta(ChannelContentSerializer.Meta):
        fields = [
            'title', 'summary', 'is_premium', 'price',
            *ChannelContentSerializer.Meta.fields,
        ]


class CompleteContentSerializer(ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, instance: ChannelContent):
        if not instance.file:
            return None
        return self.context['request'].build_absolute_uri(instance.file.file)

    class Meta:
        model = ChannelContent
        fields = [
            'text', 'file'
        ]


class FullFeatureContentSerializer(ChannelContentSerializer):

    def get_complete_content(self, instance: ChannelContent):
        return CompleteContentSerializer(
            instance,
            context=self.context,
        ).data

    class Meta(ChannelContentSerializer.Meta):
        fields = [
            'title', 'summary', 'is_premium', 'price', 'text',
            *ChannelContentSerializer.Meta.fields,
        ]


class ChannelContentSerializerConfigurer(Configurer[ChannelContentSerializer]):

    def __init__(self, ghased: Ghased, channel: Channel):
        self.ghased = ghased
        self.channel = channel

    def configure_class(self):
        raise NotImplementedError

    def configure(self, *args, **kwargs):
        kwargs['context'].update(dict(status=self.channel.get_ghased_status_wrt_channel(self.ghased)))
        return ChannelContentSerializer(*args, **kwargs)


class CreateUpdateChannelContentSerializer(ModelSerializer, metaclass=ConfiguredSecuredFileSerializerMeta):
    price = serializers.IntegerField(default=0)
    file = serializers.FileField(required=False, allow_null=True)
    securing_file_fields = ['file']
    accepted_mime_types = settings.ACCEPTED_MIME_TYPES['content_file']
    file_size_limit = settings.ACCEPTED_FILE_SIZES['content_file'] * (1 << 20)

    def create(self, validated_data):
        with transaction.atomic():
            file = validated_data.pop('file', None)
            content: ChannelContent = super().create(validated_data)
            if file:
                ContentFile.objects.create(
                    content=content,
                    file=file,
                    file_type=ContentFile.ContentFileTypes.from_mime_type(
                        self.context[self.__class__.file_security_context_key]['file_type']
                    )
                )
            return content

    def update(self, instance, validated_data):
        with transaction.atomic():
            update_or_delete = 'file' in validated_data
            file = validated_data.pop('file', None)
            content: ChannelContent = super().update(instance, validated_data)
            if update_or_delete:
                if content.file is not None:
                    if file:
                        content_file: ContentFile = content.file
                        content_file.file = File(file)
                        content_file.file_type = ContentFile.ContentFileTypes.from_mime_type(
                            self.context[self.__class__.file_security_context_key]['file_type']
                        )
                        content_file.save(update_fields=['file', 'file_type'])
                    else:
                        content_file: ContentFile = content.file
                        content_file.delete()
                        content.refresh_file()
                else:
                    if file:
                        ContentFile.objects.create(
                            content=content,
                            file=file,
                            file_type=ContentFile.ContentFileTypes.from_mime_type(
                                self.context[self.__class__.file_security_context_key]['file_type']
                            )
                        )
            return content

    class Meta:
        model = ChannelContent
        fields = [
            'title', 'summary', 'price', 'text', 'file'
        ]


class CreateContentFileSerializer(ModelSerializer, metaclass=ConfiguredSecuredFileSerializerMeta):
    securing_file_fields = ['file']
    accepted_mime_types = settings.ACCEPTED_MIME_TYPES['content_file']
    file_size_limit = settings.ACCEPTED_FILE_SIZES['content_file'] * (1 << 20)

    def validate(self, attrs):
        attrs['file_type'] = ContentFile.ContentFileTypes.from_mime_type(
            self.context[self.__class__.file_security_context_key]['file_type']
        )
        return attrs

    class Meta:
        model = ContentFile
        fields = [
            'id',
            'file',
        ]
