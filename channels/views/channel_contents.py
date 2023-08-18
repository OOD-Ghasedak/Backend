from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from accounts.models import IsGhasedPermission
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
            self.request, self.object_related,
        )


class ManagerContentsView(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [ObjectRelatedFilterset]
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhasedPermission, ]
    object_related_queryset = Channel.objects.all()
    lookup_field = 'channel_id'
    lookup_url_kwarg = 'pk'
    queryset = ChannelContent.objects.all()

    def create(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass
