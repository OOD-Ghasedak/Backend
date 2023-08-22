from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.models import Ghased
from accounts.views.serializers import UserSerializerFactory
from utility.functions import get_dict_subset


class GhasedProfilePatchSerializer(ModelSerializer):

    class Meta:
        model = Ghased
        fields = [
            'id',
            'phone_number',
            'email',
        ]


class GhasedProfileGetSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Ghased
        user_fields = ['username']
        fields = [
            'id',
            'phone_number',
            'email',
            *user_fields,
        ]
