from rest_framework.generics import ListAPIView
from rest_framework.settings import api_settings

from accounts.models import IsGhasedPermission
from subscribe.models import Subscriber
from subscribe.views.serializers import SubscribedChannelsSerializer


class SubscribedChannelsView(ListAPIView):
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        IsGhasedPermission,
    ]
    serializer_class = SubscribedChannelsSerializer

    def get_queryset(self):
        return Subscriber.objects.filter(ghased_id=self.request.ghased.id).select_related('subscription_status')
