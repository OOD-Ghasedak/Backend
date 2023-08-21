from django.db import transaction
from rest_framework import filters, status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response
from rest_framework.settings import api_settings

from accounts.models import IsGhasedPermission
from channel_management.models import IsManagerPermission
from channel_management.models.services.channel_manager_creation import ChannelManagerCreatorConfigurer, ManagerData
from channels.models import Channel
from channels.views.serializers import BaseChannelSerializer, ChannelSerializerConfigurer
from utility.django_rest_framework import GhasedakPageNumberPagination, GenericViewSet


class ChannelsView(
    DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, GenericViewSet,
):
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    queryset = Channel.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        IsGhasedPermission,
    ]

    def get_permission_classes(self):
        added_permissions = []
        if not self.is_read_only_action():
            added_permissions += [IsManagerPermission]
        return [
            *self.permission_classes,
            *added_permissions,
        ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ChannelSerializerConfigurer(
                mode=ChannelSerializerConfigurer.Mode.FULL
            ).configure_class()
        return ChannelSerializerConfigurer(
            mode=ChannelSerializerConfigurer.Mode.CREATE
        ).configure_class()

    def create(self, request, *args, **kwargs):
        channel_manager_configurer = ChannelManagerCreatorConfigurer(ChannelManagerCreatorConfigurer.Sources.OWNER)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            channel = serializer.save()
            channel_manager_configurer.configure(ManagerData(ghased=request.user.ghased, channel=channel)).create()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(ghased=request.user.ghased)
        return Response(serializer.data)


class SearchChannelPagination(GhasedakPageNumberPagination):
    page_size = 20
    max_page_size = 50


class SearchChannelView(ListModelMixin, GenericViewSet):
    pagination_class = SearchChannelPagination
    queryset = Channel.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        IsGhasedPermission,
    ]
    serializer_class: BaseChannelSerializer = ChannelSerializerConfigurer(
        mode=ChannelSerializerConfigurer.Mode.FULL
    ).configure_class()
