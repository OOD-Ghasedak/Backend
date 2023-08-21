from rest_framework.mixins import DestroyModelMixin
from rest_framework.settings import api_settings

from accounts.models import IsGhasedPermission
from channel_management.models import IsOwnerPermission
from channels.models import Subscription, Channel
from channels.views.serializers import OwnerSubscriptionSerializer
from utility.django_rest_framework import ObjectRelatedFilterset, GenericViewSet, ListModelMixin, CreateModelMixin


class ChannelOwnerSubscriptionsView(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet,
):
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [ObjectRelatedFilterset]
    object_related_queryset = Channel.objects.all()
    related_lookup_field = 'channel_id'
    related_lookup_url_kwarg = 'channel_pk'
    queryset = Subscription.objects.all()
    serializer_class = OwnerSubscriptionSerializer

    def get_permission_classes(self):
        permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhasedPermission]
        if self.action != 'list':
            permission_classes += [IsOwnerPermission]
        return permission_classes

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'channel': self.related_object,
        }

    def get_serializer(self, *args, **kwargs):
        kwargs.update(dict(many=True))
        return super().get_serializer(*args, **kwargs)

    def get_object(self):
        related_obj = ObjectRelatedFilterset().get_related_object(self)
        self.check_object_permissions(self.request, related_obj)
        return self.filter_queryset(self.get_queryset())

    def perform_destroy(self, instances):
        for instance in instances:
            instance.delete()
