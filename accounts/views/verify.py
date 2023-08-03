from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from accounts.models import RegisterOTP
from accounts.views.serializers import RegisterOTPSerializer


class VerifyForRegisterView(
    CreateModelMixin, GenericViewSet
):
    queryset = RegisterOTP.objects.all()
    serializer_class = RegisterOTPSerializer
    permission_classes = []

