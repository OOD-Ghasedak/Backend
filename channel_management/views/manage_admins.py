from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.settings import api_settings

from accounts.models import IsGhasedPermission
from channel_management.models import IsOwnerPermission, ChannelAdmin
from channel_management.views.serializers import ChannelAdminSerializer
from channels.models import Channel
from utility.django_rest_framework import GenericViewSet, CreateModelMixin, ObjectRelatedFilterset


class CreateAdminsView(CreateModelMixin, GenericViewSet):
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [ObjectRelatedFilterset]
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhasedPermission, IsOwnerPermission]
    object_related_queryset = Channel.objects.all()
    related_lookup_field = 'channel_id'
    related_lookup_url_kwarg = 'channel_pk'
    lookup_field = 'id'
    lookup_url_kwarg = 'pk'
    queryset = ChannelAdmin.objects.all()
    serializer_class = ChannelAdminSerializer

    def perform_create(self, serializer):
        serializer.save(channel=self.related_object)


class DestroyUpdateAdminsView(UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhasedPermission, IsOwnerPermission]
    object_related_queryset = Channel.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'pk'
    queryset = ChannelAdmin.objects.all()
    serializer_class = ChannelAdminSerializer

    def check_object_permissions(self, request, obj):
        return super(DestroyUpdateAdminsView, self).check_object_permissions(request, obj.channel)
