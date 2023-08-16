from rest_framework.mixins import ListModelMixin
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from accounts.models import IsGhasedPermission
from channels.models import ChannelContent
from utility.django_rest_framework import ObjectRelatedFilterset


class ContentsView(ListModelMixin, GenericViewSet):
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [ObjectRelatedFilterset]
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhasedPermission]
    lookup_field = 'channel_id'
    lookup_url_kwarg = 'pk'
    queryset = ChannelContent.objects.all()

    def get_serializer_class(self):


