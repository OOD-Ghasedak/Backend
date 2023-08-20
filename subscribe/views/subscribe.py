from django.db import transaction
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_201_CREATED, HTTP_402_PAYMENT_REQUIRED
from rest_framework.viewsets import GenericViewSet

from accounts.models import IsGhasedPermission, Ghased
from channels.models import Channel, Subscription
from financial.facade import FinancialFacade
from subscribe.views.serializers.subscribe import SubscriberSerializer, PremiumSubscriberSerializer
from utility.django_rest_framework import ObjectRelatedFilterset


class SubscriberView(CreateModelMixin, GenericViewSet):
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        IsGhasedPermission,
    ]
    object_related_queryset = Channel.objects.all()
    related_lookup_field = 'channel_id'
    related_lookup_url_kwarg = 'channel_pk'
    serializer_class = SubscriberSerializer

    def get_related_object(self):
        obj = ObjectRelatedFilterset().get_related_object(self)
        self.check_object_permissions(self.request, obj)
        self.related_object = obj
        return obj

    def create(self, request, *args, **kwargs):
        channel: Channel = self.get_related_object()
        if channel.subscriptions.exists():
            return Response(data={"msg":"باید اشتراک خریداری شود"}, status=HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(channel_id=channel.id, ghased_id=request.user.ghased.id, data={
            'subscription_status': {}
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_201_CREATED)


class PremiumSubscriberView(SubscriberView):
    serializer_class = PremiumSubscriberSerializer

    def create(self, request, *args, **kwargs):
        ghased: Ghased = request.user.ghased
        channel: Channel = self.get_related_object()
        subscription: Subscription = get_object_or_404(Subscription.objects.all(), id=self.kwargs['subscription_pk'])
        serializer = self.get_serializer(subscription=subscription, channel_id=channel.id,
                                         ghased_id=ghased.id, data={'subscription_status': {}})
        if ghased.wallet.balance < subscription.price:
            return Response(data={'msg': 'موجودی ناکافی'}, status=HTTP_402_PAYMENT_REQUIRED)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save()
            financial_facade = FinancialFacade.get_instance()
            financial_facade.transact(ghased.wallet, channel.owner.ghased.wallet, subscription.price)
        return Response(status=HTTP_201_CREATED)
