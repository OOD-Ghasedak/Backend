from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from accounts.models import IsGhasedPermission
from financial.views.serializers import WalletSerializer, DepositSerializer, WithdrawSerializer


class WalletView(RetrieveAPIView):
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        IsGhasedPermission,
    ]
    serializer_class = WalletSerializer

    def get_object(self):
        return self.request.ghased.wallet


class DepositView(CreateModelMixin, GenericViewSet):
    serializer_class = DepositSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        IsGhasedPermission,
    ]

    def perform_create(self, serializer):
        serializer.save(wallet=self.request.user.ghased.wallet)


class WithdrawView(CreateModelMixin, GenericViewSet):
    serializer_class = WithdrawSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        IsGhasedPermission,
    ]

    def perform_create(self, serializer):
        serializer.save(wallet=self.request.user.ghased.wallet)
