from rest_framework.generics import RetrieveAPIView
from rest_framework.settings import api_settings

from accounts._ports.permissions import PermissionsFacade as AccountsPermissionsFacade
from financial.views.serializers import WalletSerializer


class WalletView(RetrieveAPIView):
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        AccountsPermissionsFacade.get_instance().get_ghased_permission_class()
    ]
    serializer_class = WalletSerializer

    def get_object(self):
        return self.request.ghased.wallet
