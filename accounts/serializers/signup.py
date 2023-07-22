from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.models import Ghased


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model()(**validated_data)
        user.set_password(password)
        user.save()
        return user


class GhasedSignupSerializer(ModelSerializer):
    username = serializers.CharField(max_length=50)
    phone_number = serializers.CharField(max_length=11)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        user_serializer = UserSerializer(data=validated_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        ghased = Ghased.objects.create(user=user, phone_number=phone_number)
        return ghased

    def validate_phone_number(self, value):
        if len(value) != 11:
            raise serializers.ValidationError("phone_number is not valid format")
        # todo: other checks if needed
        return value

    class Meta:
        model = Ghased
        fields = [
            'username',
            'email',
            'password',
            'phone_number',
        ]
