from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, \
    RetrieveModelMixin
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from accounts.models import IsGhasedPermission
from channel_management.models import IsManagerPermission
from channels.models import ChannelContent, Channel, ContentFile
from channels.views.serializers import ChannelContentSerializerConfigurer, CreateUpdateChannelContentSerializer
from channels.views.serializers.channel_contents import CreateContentFileSerializer
from utility.django_rest_framework import ObjectRelatedFilterset, GhasedakPageNumberPagination


class ChannelContentsPagination(GhasedakPageNumberPagination):
    page_size = 20
    max_page_size = 50


class CreateListContentsView(ListModelMixin, CreateModelMixin, GenericViewSet):
    pagination_class = ChannelContentsPagination
    ordering = ['created']
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [ObjectRelatedFilterset, OrderingFilter]
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhasedPermission]
    object_related_queryset = Channel.objects.all()
    related_lookup_field = 'channel_id'
    related_lookup_url_kwarg = 'channel_pk'
    queryset = ChannelContent.objects.all()

    def get_permissions(self):
        permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhasedPermission]
        if self.action != 'list':
            permission_classes += [IsManagerPermission]
        return [permission() for permission in permission_classes]

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action == 'list':
            return ChannelContentSerializerConfigurer(
                self.request.ghased, self.related_object,
            ).configure(*args, **kwargs)
        return CreateUpdateChannelContentSerializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(channel=self.related_object)


class UpdateDestroyContentsView(UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhasedPermission, IsManagerPermission]
    lookup_field = 'id'
    lookup_url_kwarg = 'pk'
    queryset = ChannelContent.objects.all()
    serializer_class = CreateUpdateChannelContentSerializer

    def check_object_permissions(self, request, obj):
        return super(UpdateDestroyContentsView, self).check_object_permissions(request, obj.channel)

    def get_object(self):
        return super(UpdateDestroyContentsView, self).get_object()
