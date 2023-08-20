from django.db import transaction
from rest_framework import filters, status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from accounts.models import IsGhasedPermission
from channel_management.models import IsManagerPermission
from channel_management.models.services.channel_manager_creation import ChannelManagerCreatorConfigurer, ManagerData
from channels.models import Channel
from channels.views.serializers import BaseChannelSerializer, ChannelSerializerConfigurer
from utility.django_rest_framework import GhasedakPageNumberPagination


class CreateChannelView(
    RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, GenericViewSet,
):
    lookup_field = 'pk'
    queryset = Channel.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        IsGhasedPermission,
        IsManagerPermission,
    ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ChannelSerializerConfigurer(
                mode=ChannelSerializerConfigurer.Mode.GHASED_VIEW
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
        mode=ChannelSerializerConfigurer.Mode.SUMMARY
    ).configure_class()
