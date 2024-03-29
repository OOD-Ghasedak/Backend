from rest_framework.generics import ListAPIView
from rest_framework.settings import api_settings

from accounts.models import IsGhasedPermission
from channel_management.models import ChannelManager
from channel_management.views.serializers import ManagedChannelsSerializer


class ManagedChannelsView(ListAPIView):
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        IsGhasedPermission,
    ]
    serializer_class = ManagedChannelsSerializer

    def get_queryset(self):
        return ChannelManager.concrete_objects.filter(
            ghased_id=self.request.ghased.id
        )
