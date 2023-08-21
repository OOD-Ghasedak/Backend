from rest_framework.settings import api_settings

from accounts.models import IsGhasedPermission
from subscribe.models import PurchasedSubscription, PurchasedContent
from subscribe.views.serializers import PurchasedSubscriptionSerializer, PurchasedContentSerializer
from utility.django_rest_framework import GenericViewSet, CreateModelMixin


class PurchasedSubscriptionView(CreateModelMixin, GenericViewSet):
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhasedPermission]
    queryset = PurchasedSubscription.objects.all()
    serializer_class = PurchasedSubscriptionSerializer


class PurchasedContentView(CreateModelMixin, GenericViewSet):
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhasedPermission]
    queryset = PurchasedContent.objects.all()
    serializer_class = PurchasedContentSerializer
