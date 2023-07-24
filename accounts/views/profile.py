from rest_framework.exceptions import ValidationError
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.viewsets import GenericViewSet

from accounts.models import Ghased
from accounts.views.permissions import IsGhased
from accounts.views.serializers import GhasedProfilePatchSerializer, GhasedProfileGetSerializer


class GhasedProfileView(
    UpdateModelMixin, RetrieveModelMixin, GenericViewSet
):
    queryset = Ghased.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhased]

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return GhasedProfilePatchSerializer
        if self.action == 'retrieve':
            return GhasedProfileGetSerializer
        raise ValidationError(
            'متد روی این مسیر قابل اجرا نیست!',
            code=HTTP_405_METHOD_NOT_ALLOWED,
        )

    def get_object(self):
        return self.request.ghased
