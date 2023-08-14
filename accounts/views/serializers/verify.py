from rest_framework.serializers import ModelSerializer

from accounts.models import RegisterOTP


class RegisterOTPSerializer(ModelSerializer):

    def validate(self, attrs):
        if not (bool(attrs.get('email')) or bool(attrs.get('phone_number'))):
            # TODO: Raise correct error
            pass
        return attrs

    def create(self, validated_data):
        return RegisterOTP.generate_register_otp(**validated_data)

    def to_representation(self, instance: RegisterOTP):
        return {
            'otp': instance.otp.code,
        }

    class Meta:
        model = RegisterOTP
        fields = [
            'email',
            'phone_number',
        ]
