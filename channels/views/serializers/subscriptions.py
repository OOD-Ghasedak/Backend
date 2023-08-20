from rest_framework.serializers import ModelSerializer, ListSerializer

from channels.models import Subscription


class OwnerSubscriptionListSerializer(ListSerializer):

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        res = []
        for attrs in validated_data:
            attrs.update(dict(
                channel=self.context['channel'],
            ))
            res.append(self.child.create(attrs))
        return res


class OwnerSubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        list_serializer_class = OwnerSubscriptionListSerializer
        fields = [
            'id',
            'price',
            'duration_choice',
        ]
