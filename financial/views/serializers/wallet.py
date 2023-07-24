from rest_framework.serializers import ModelSerializer

from financial.models import Wallet


class WalletSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            'id',
            'balance',
        ]
