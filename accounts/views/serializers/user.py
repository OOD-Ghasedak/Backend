from typing import Type

from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


class UserSerializerFactory:

    def __init__(self, fields):
        self.fields = fields

    def get_serializer(self) -> Type[ModelSerializer]:
        class UserSerializer(ModelSerializer):
            class Meta:
                model = get_user_model()
                fields = self.fields

        return UserSerializer
