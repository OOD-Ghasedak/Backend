from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import DestroyModelMixin
from rest_framework.settings import api_settings

from accounts.models import IsGhasedPermission
from channels.models import Channel
from subscribe.models import Subscriber
from subscribe.models.subscriber import IsSubscriberPermission
from subscribe.views.serializers import SubscriberSerializer
from utility.django_rest_framework import GenericViewSet, CreateModelMixin, ObjectRelatedFilterset
from utility.models.managers import filter_active_objects


class SubscribeView(DestroyModelMixin, CreateModelMixin, GenericViewSet):
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [ObjectRelatedFilterset]
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhasedPermission]
    object_related_queryset = Channel.objects.all()
    related_lookup_field = 'channel_id'
    related_lookup_url_kwarg = 'channel_pk'
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

    def get_permission_classes(self):
        if self.action == 'create':
            return self.permission_classes
        elif self.action == 'destroy':
            return [
                *self.permission_classes,
                IsSubscriberPermission,
            ]
        raise MethodNotAllowed(self.request.method)

    def perform_create(self, serializer):
        serializer.save(channel=self.related_object, ghased=self.request.ghased)

    def get_object(self):
        channel = get_object_or_404(Channel.objects.all(), id=self.kwargs['channel_pk'])
        return get_object_or_404(filter_active_objects(channel.subscribers), ghased_id=self.request.ghased.id)

