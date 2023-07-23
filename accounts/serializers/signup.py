from rest_framework import serializers

from accounts.models import Ghased
from accounts.models.services.ghased_creation import GhasedCreatorConfigurer, GhasedData, GhasedCreatorInterface
from utility.django import GhasedakMobileNumberValidator


class GhasedSignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    phone_number = serializers.CharField(max_length=11, validators=[GhasedakMobileNumberValidator(
        message='شماره همراه باید ۱۱ رقمی باشد و با ۰۹ آغاز گردد.'
    )])
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)

    def create(self, validated_data) -> Ghased:
        creator: GhasedCreatorInterface = GhasedCreatorConfigurer(GhasedCreatorConfigurer.Sources.SIGN_UP).configure(
            GhasedData(**validated_data)
        )
        return creator.create()

    def update(self, instance, validated_data):
        raise NotImplementedError

    def to_representation(self, instance: Ghased):
        return {
            'username': instance.user.username,
            'email': instance.user.email,
            'phone_number': instance.user.phone_number,
        }
