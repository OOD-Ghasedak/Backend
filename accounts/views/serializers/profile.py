from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.models import Ghased
from accounts.views.serializers import UserSerializerFactory
from utility.functions import get_dict_subset


class GhasedProfilePatchSerializer(ModelSerializer):

    def update(self, instance: Ghased, validated_data):
        with transaction.atomic():
            user_serializer = UserSerializerFactory(self.Meta.user_fields).get_serializer()(
                instance=instance.user,
                data=get_dict_subset(validated_data, self.Meta.user_fields, False),
                partial=True,
            )
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
            return super().update(instance, validated_data)

    class Meta:
        model = Ghased
        user_fields = ['email']
        fields = [
            'id',
            'phone_number',
            *user_fields,
        ]


class GhasedProfileGetSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Ghased
        user_fields = ['email', 'username']
        fields = [
            'id',
            'phone_number',
            *user_fields,
        ]
