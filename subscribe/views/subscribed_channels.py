from rest_framework.generics import ListAPIView
from rest_framework.settings import api_settings

from accounts._ports.permissions import PermissionsFacade as AccountsPermissionsFacade
from subscribe.models import Subscriber
from subscribe.views.serializers import SubscribedChannelsSerializer


class SubscribedChannelsView(ListAPIView):
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        AccountsPermissionsFacade.get_instance().get_ghased_permission_class()
    ]
    serializer_class = SubscribedChannelsSerializer

    def get_queryset(self):
        return Subscriber.objects.filter(ghased_id=self.request.ghased.id).select_related('subscription_status')
