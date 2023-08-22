from typing import TYPE_CHECKING

from django.db.models import Sum
from rest_framework.serializers import ModelSerializer
from rest_framework.status import HTTP_424_FAILED_DEPENDENCY

from channel_management.models import ChannelAdmin
from utility.django_rest_framework import ValidationError
from utility.models.managers import filter_active_objects

if TYPE_CHECKING:
    from channels.models import Channel

class ChannelAdminSerializer(ModelSerializer):

    def create(self, validated_data):
        ghased, channel, share = validated_data['ghased'], validated_data['channel'], validated_data['share']
        admins = filter_active_objects(channel.admins)
        if admins.filter(ghased_id=ghased):
            raise ValidationError({'message': 'قاصد پیش‌تر در این کانال دارای نقش مدیر می‌باشد!'},
                                  status_code=HTTP_424_FAILED_DEPENDENCY)
        current_total_share = admins.aggregate(current_total_share=Sum('share')).get('current_total_share') or 0
        if current_total_share + share > 100:
            raise ValidationError({'message': 'مجموع سهم مدیران بیش از ۱۰۰ درصد خواهد شد.'})
        return super().create(validated_data)

    class Meta:
        model = ChannelAdmin
        fields = [
            'ghased',
            'share',
        ]


class UpdateShareAdminSerializer(ModelSerializer):
    def validate_share(self, value: float):
        channel: 'Channel' = self.instance.channel
        admins = filter_active_objects(channel.admins).exclude(id=self.instance.id)
        current_total_share = admins.aggregate(current_total_share=Sum('share')).get('current_total_share') or 0
        if current_total_share + value > 100:
            raise ValidationError({'message': 'مجموع سهم مدیران بیش از ۱۰۰ درصد خواهد شد.'})
        return value

    class Meta:
        model = ChannelAdmin
        fields = [
            'share',
        ]
