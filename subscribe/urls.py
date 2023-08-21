from django.urls import path

from subscribe.views import SubscribedChannelsView, SubscribeView, PurchasedSubscriptionView, PurchasedContentView

urlpatterns = [
    path('joined-channels/', SubscribedChannelsView.as_view()),
    path('<int:channel_pk>/', SubscribeView.as_view(
        {
            'post': 'create',
            'delete': 'destroy'
        }
    )),
    path('purchased-subscriptions/', PurchasedSubscriptionView.as_view({
        'post': 'create',
    })),
    path('purchased-contents/', PurchasedContentView.as_view({
        'post': 'create',
    }))
]
