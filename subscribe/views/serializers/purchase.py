from typing import TYPE_CHECKING

from django.db import transaction
from rest_framework import status
from rest_framework.serializers import ModelSerializer

from financial.models import Transaction
from subscribe.models import PurchasedSubscription, PurchasedContent
from utility.django_rest_framework import ValidationError
from utility.models.managers import filter_active_objects

if TYPE_CHECKING:
    from channels.models import Subscription, ChannelContent


class BasePurchaseSerializer(ModelSerializer):
    _purchasable_field = None

    @property
    def ghased(self):
        return self.context['request'].ghased

    def validate_purchasable(self, value):
        if value.price > self.ghased.wallet.balance:
            raise ValidationError({'message': 'موجودی حساب کافی نیست'}, status_code=status.HTTP_402_PAYMENT_REQUIRED)
        subscriber = filter_active_objects(value.channel.subscribers).filter(ghased_id=self.ghased.id).first()
        if subscriber is None:
            raise ValidationError({'message': 'شما عضو این کانال نیستید.'})
        self.context['subscriber'] = subscriber
        return value

    def create(self, validated_data):
        with transaction.atomic():
            purchasable = validated_data[self._purchasable_field]
            owner = purchasable.channel.owner
            tr = Transaction.pay(self.ghased.wallet, owner.ghased.wallet, amount=purchasable.price)
            owner.pay_to_admins(tr)
            validated_data['subscriber'] = self.context['subscriber']
            return super().create(validated_data)


class PurchasedSubscriptionSerializer(BasePurchaseSerializer):
    _purchasable_field = 'subscription'

    def validate_subscription(self, value: 'Subscription'):
        return self.validate_purchasable(value)

    class Meta:
        model = PurchasedSubscription
        fields = [
            'subscription'
        ]


class PurchasedContentSerializer(BasePurchaseSerializer):
    _purchasable_field = 'content'

    @property
    def ghased(self):
        return self.context['request'].ghased

    def validate_content(self, value: 'ChannelContent'):
        if not value.is_premium:
            raise ValidationError({'message': 'این محتوا برای خریدن نیست!'})

        return self.validate_purchasable(value)

    class Meta:
        model = PurchasedContent
        fields = [
            'content',
        ]
