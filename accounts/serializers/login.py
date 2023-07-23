from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_401_UNAUTHORIZED


class GhasedLoginSerializer(Serializer):
    email_or_username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128)

    def is_valid_email(self, email):
        try:
            validate_email(email)
            return True
        except DjangoValidationError:
            return False

    def validate(self, attrs):
        email_or_username, password = attrs['email_or_username'], attrs['password']
        ghased_user = get_object_or_404(
            get_user_model().objects.all(),
            email=email_or_username
        ) if self.is_valid_email(email_or_username) else get_object_or_404(
            get_user_model().objects.all(),
            username=email_or_username
        )
        attrs['username'] = ghased_user.username

        if not check_password(password, ghased_user.password):
            raise ValidationError(
                {'password': 'رمز عبور اشتباه است'},
                code=HTTP_401_UNAUTHORIZED
            )

        return attrs
