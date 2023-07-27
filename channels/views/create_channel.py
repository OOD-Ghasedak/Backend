from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from accounts._ports.permissions import PermissionsFacade as AccountsPermissionsFacade
from channels.models import Channel
from channels.views.permissions import IsManager
from channels.views.serializers import BaseChannelSerializer, ChannelSerializerConfigurer


class CreateChannelView(
    UpdateModelMixin, CreateModelMixin, GenericViewSet,
):
    lookup_field = 'pk'
    queryset = Channel.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        AccountsPermissionsFacade.get_instance().get_ghased_permission_class(),
        IsManager,
    ]
    serializer_class: BaseChannelSerializer = ChannelSerializerConfigurer(
        mode=ChannelSerializerConfigurer.Mode.CREATE
    ).configure_class()
