
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from accounts.views.permissions import IsGhased
from channels.models import Subscription
from channels.views.permissions import IsOwner
from channels.views.serializers import OwnerSubscriptionSerializer


class ChannelOwnerSubscriptionsView(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet,
):
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhased, IsOwner]
    lookup_field = 'channel_id'
    lookup_url_kwarg = 'pk'
    queryset = Subscription.objects.all()
    serializer_class = OwnerSubscriptionSerializer

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'channel': self.kwargs[self.lookup_url_kwarg],
        }

    def get_serializer(self, *args, **kwargs):
        kwargs.update(dict(many=True))
        return super().get_serializer(*args, **kwargs)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        return queryset.filter(**filter_kwargs)

    def get_object(self):
        return self.filter_queryset(self.get_queryset())

    def perform_destroy(self, instances):
        for instance in instances:
            instance.delete()


