from rest_framework.serializers import ModelSerializer

from financial.models import TransactionEntry
from financial.models import Wallet


class WalletSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            'id',
            'balance',
        ]


class DepositSerializer(ModelSerializer):
    class Meta:
        model = TransactionEntry
        fields = ['amount']


class WithdrawSerializer(ModelSerializer):
    class Meta:
        model = TransactionEntry
        fields = ['amount']

    def validate(self, attrs):
        attrs['amount'] = -attrs['amount']
        return attrs
