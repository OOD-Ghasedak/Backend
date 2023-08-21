from rest_framework.serializers import ModelSerializer
from rest_framework.status import HTTP_424_FAILED_DEPENDENCY

from subscribe.models import Subscriber
from utility.django_rest_framework import ValidationError


class SubscriberSerializer(ModelSerializer):

    def save(self, *, channel, ghased):
        if channel.get_ghased_status_wrt_channel(ghased) is not None:
            raise ValidationError({'message': 'قاصد پیش‌تر در این کانال دارای نقش شده است!'},
                                  status_code=HTTP_424_FAILED_DEPENDENCY)
        return super().save(channel=channel, ghased=ghased)

    class Meta:
        model = Subscriber
        fields = [
        ]
