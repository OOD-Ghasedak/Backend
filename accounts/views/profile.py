from rest_framework.exceptions import MethodNotAllowed
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from accounts.models import Ghased, IsGhasedPermission
from accounts.views.serializers import GhasedProfilePatchSerializer, GhasedProfileGetSerializer


class GhasedProfileView(
    UpdateModelMixin, RetrieveModelMixin, GenericViewSet
):
    queryset = Ghased.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhasedPermission]

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return GhasedProfilePatchSerializer
        if self.action == 'retrieve':
            return GhasedProfileGetSerializer
        raise MethodNotAllowed(self.request.method)

    def get_object(self):
        return self.request.ghased
