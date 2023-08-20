from django.urls import path

from subscribe.views import SubscribedChannelsView, SubscriberView, PremiumSubscriberView

urlpatterns = [
    path('joined-channels/', SubscribedChannelsView.as_view()),
    path('<int:channel_pk>/subscribe/', SubscriberView.as_view({
        'post': 'create',
    })),
    path('<int:channel_pk>/subscribe/<int:subscription_pk>/', PremiumSubscriberView.as_view({
        'post': 'create',
    })),
]
