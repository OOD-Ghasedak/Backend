from rest_framework import serializers

from accounts.models import Ghased
from accounts.models.services.ghased_creation import GhasedCreatorConfigurer, GhasedData, GhasedCreatorInterface
from accounts.views.serializers import UserSerializerFactory
from utility.functions import get_dict_subset


class GhasedSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)

    def create(self, validated_data) -> Ghased:
        user = UserSerializerFactory(self.Meta.user_fields).get_serializer()(
            data=get_dict_subset(validated_data, self.Meta.user_fields)
        )
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
        user_fields = ['username', 'email', 'password']
        fields = [user_fields, 'phone_number', ]
