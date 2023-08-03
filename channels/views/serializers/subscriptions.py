from rest_framework.serializers import ModelSerializer, ListSerializer


class OwnerSubscriptioListSerializer(ListSerializer):

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
        list_serializer_class = OwnerSubscriptioListSerializer
        fields = [
            'price',
            'channel',
            'duration_choice',
        ]
