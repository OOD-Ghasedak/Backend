from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from accounts.models import IsGhasedPermission
from channel_management.models import IsManagerPermission
from channels.models import ChannelContent, Channel
from channels.views.serializers import ChannelContentSerializerConfigurer
from utility.django_rest_framework import ObjectRelatedFilterset, GhasedakPageNumberPagination


class ChannelContentsPagination(GhasedakPageNumberPagination):
    page_size = 10
    max_page_size = 20


class ChannelContentsView(ListModelMixin, GenericViewSet):
    pagination_class = ChannelContentsPagination
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [ObjectRelatedFilterset]
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhasedPermission]
    object_related_queryset = Channel.objects.all()
    lookup_field = 'channel_id'
    lookup_url_kwarg = 'pk'
    queryset = ChannelContent.objects.all()

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        return ChannelContentSerializerConfigurer(
            self.request, ObjectRelatedFilterset().get_related_object(self),
        )


class ManagerCreateContentsView(UpdateModelMixin, CreateModelMixin, GenericViewSet):
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [ObjectRelatedFilterset]
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhasedPermission, IsManagerPermission]
    object_related_queryset = Channel.objects.all()
    lookup_field = 'channel_id'
    lookup_url_kwarg = 'pk'
    queryset = ChannelContent.objects.all()

    def check_object_permissions(self, request, obj):
        if isinstance(obj, Channel):
            return super(ManagerCreateContentsView, self).check_object_permissions(request, obj)
        if isinstance(obj, ChannelContent):
            return super(ManagerCreateContentsView, self).check_object_permissions(request, obj.channel)

    def get_related_object(self):
        obj = ObjectRelatedFilterset().get_related_object(self)
        self.check_object_permissions(self.request, obj)
        self.related_object = obj
        return obj

    def get_object(self):
        self.get_related_object()
        return super(ManagerCreateContentsView, self).get_object()

    def create(self, request, *args, **kwargs):
        self.get_related_object()
        return super(ManagerCreateContentsView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(channel=self.related_object)

    def perform_update(self, serializer):
        serializer.save(channel=self.related_object)

