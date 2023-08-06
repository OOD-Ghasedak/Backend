from rest_framework.generics import RetrieveAPIView
from rest_framework.settings import api_settings

from accounts.models import IsGhasedPermission
from financial.views.serializers import WalletSerializer


class WalletView(RetrieveAPIView):
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        IsGhasedPermission,
    ]
    serializer_class = WalletSerializer

    def get_object(self):
        return self.request.ghased.wallet
