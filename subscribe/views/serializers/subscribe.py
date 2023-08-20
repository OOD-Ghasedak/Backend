from django.db import transaction
from rest_framework.serializers import ModelSerializer

from subscribe.models import Subscriber, PurchasedSubscription


class SubscriberSerializer(ModelSerializer):

    def __init__(self, channel_id, ghased_id, **kwargs):
        super().__init__(**kwargs)
        self.channel_id = channel_id
        self.ghased_id = ghased_id

    def create(self, validated_data):
        return Subscriber.objects.create(channel_id=self.channel_id, ghased_id=self.ghased_id)

    class Meta:
        model = Subscriber
        fields = []


class PremiumSubscriberSerializer(SubscriberSerializer):

    def __init__(self, subscription, **kwargs):
        super().__init__(**kwargs)
        self.subscription = subscription

    def create(self, validated_data):
        if subscriber := Subscriber.objects.filter(channel_id=self.channel_id, ghased_id=self.ghased_id).first():
            PurchasedSubscription.objects.create(subscriber=subscriber, subscription=self.subscription)
        else:
            subscriber = super().create(validated_data)
            PurchasedSubscription.objects.create(subscriber=subscriber, subscription=self.subscription)

        return subscriber
