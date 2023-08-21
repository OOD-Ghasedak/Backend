from rest_framework.mixins import ListModelMixin
from rest_framework.settings import api_settings

from accounts.models import IsGhasedPermission
from channel_management.models import ChannelAdmin, IsOwnerPermission
from channels.models import Channel
from utility.django_rest_framework import GenericViewSet, ObjectRelatedFilterset


class ChannelAdminsView(ListModelMixin, GenericViewSet):
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [ObjectRelatedFilterset]
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhasedPermission, IsOwnerPermission]
    object_related_queryset = Channel.objects.all()
    related_lookup_field = 'channel_id'
    related_lookup_url_kwarg = 'channel_pk'
    queryset = ChannelAdmin.objects.all()
    serializer_class = None  # TODO

