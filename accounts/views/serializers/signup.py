from collections import OrderedDict

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from accounts.models import Ghased, RegisterOTP
from accounts.models.services.ghased_creation import GhasedCreatorConfigurer, GhasedData, GhasedCreatorInterface
from accounts.views.serializers import UserSerializerFactory
from utility.functions import get_dict_subset


class GhasedSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128)
    otp = serializers.CharField(max_length=128)

    def validate_otp(self, value):
        try:
            return RegisterOTP.get_from_otp_code(value)
        except RegisterOTP.DoesNotExist:
            # TODO: Raise correct error
            pass

    def create(self, validated_data) -> Ghased:
        user = UserSerializerFactory(self.Meta.user_fields).get_serializer()(
            data=get_dict_subset(validated_data, self.Meta.user_fields)
        )
        user.is_valid(raise_exception=True)
        creator: GhasedCreatorInterface = GhasedCreatorConfigurer(GhasedCreatorConfigurer.Sources.SIGN_UP).configure(
            validated_data['username'], validated_data['password'], validated_data['otp'],
        )
        return creator.create()

    def update(self, instance, validated_data):
        raise NotImplementedError

    def to_representation(self, instance: Ghased):
        return OrderedDict({
            'username': instance.user.username,
            'email': instance.user.email,
            'phone_number': instance.user.phone_number,
        })

    class Meta:
        model = Ghased
        user_fields = ['username', 'password']
        fields = [*user_fields, 'otp']
