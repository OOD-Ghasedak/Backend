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

    def get_serializer(self, *args, **kwargs):
        data = kwargs['data']
        data.update(dict(
            wallet=self.request.ghased.wallet_id
        ))
        kwargs['data'] = data
        return super(DepositView, self).get_serializer(*args, **kwargs)


class WithdrawView(CreateModelMixin, GenericViewSet):
    serializer_class = WithdrawSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        IsGhasedPermission,
    ]

    def get_serializer(self, *args, **kwargs):
        data = kwargs['data']
        data.update(dict(
            wallet=self.request.ghased.wallet_id
        ))
        kwargs['data'] = data
        return super(WithdrawView, self).get_serializer(*args, **kwargs)
