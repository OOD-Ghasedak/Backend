from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import Ghased
from accounts.models.services.ghased_creation import GhasedCreatorConfigurer, GhasedData, GhasedCreatorInterface
from utility.django import GhasedakMobileNumberValidator
from utility.functions import get_dict_subset


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'username']


class GhasedSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)

    def create(self, validated_data) -> Ghased:
        user = UserSerializer(data=get_dict_subset(validated_data, UserSerializer.Meta.fields))
        user.is_valid(raise_exception=True)
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

    class Meta:
        model = Ghased
        fields = ['username', 'email', 'phone_number', 'password']
