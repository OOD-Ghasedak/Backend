from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from accounts.models import Ghased
from accounts.view.permissions import IsGhased
from accounts.view.serializers import GhasedProfilePatchSerializer, GhasedProfileGetSerializer


class AthleteProfileView(
    UpdateModelMixin, RetrieveModelMixin, GenericViewSet
):
    queryset = Ghased.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhased]

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return GhasedProfilePatchSerializer
        return GhasedProfileGetSerializer

    def get_object(self):
        return self.request.ghased
