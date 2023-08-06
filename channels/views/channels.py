from rest_framework import filters
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from accounts.models import IsGhasedPermission
from channels.models import Channel
from channels.views.permissions import IsManagerPermission
from channels.views.serializers import BaseChannelSerializer, ChannelSerializerConfigurer


class CreateChannelView(
    UpdateModelMixin, CreateModelMixin, GenericViewSet,
):
    lookup_field = 'pk'
    queryset = Channel.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        IsGhasedPermission,
        IsManagerPermission,
    ]
    serializer_class: BaseChannelSerializer = ChannelSerializerConfigurer(
        mode=ChannelSerializerConfigurer.Mode.CREATE
    ).configure_class()


class SearchChannelView(ListModelMixin, GenericViewSet):
    # TODO: add paginator when needed
    queryset = Channel.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        IsGhasedPermission,
    ]
    serializer_class: BaseChannelSerializer = ChannelSerializerConfigurer(
        mode=ChannelSerializerConfigurer.Mode.SUMMARY
    ).configure_class()
