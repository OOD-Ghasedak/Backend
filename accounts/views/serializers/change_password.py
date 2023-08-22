from django.contrib.auth.models import User
from rest_framework import serializers

from utility.django_rest_framework import ValidationError


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)

    def validate_old_password(self, value: str):
        user: User = self.instance.user
        if not user.check_password(value):
            raise ValidationError({'message': 'رمز عبور پیشین اشتباه است!'})
        return value

    def update(self, instance, validated_data):
        user: User = self.instance.user
        user.set_password(validated_data['new_password'])
        user.save(update_fields=['password'])
        return user
