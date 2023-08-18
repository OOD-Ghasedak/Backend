from django.urls import path

from channels.views import (
    ChannelOwnerSubscriptionsView,
    CreateChannelView,
    SearchChannelView,
    ChannelContentsView,
)

urlpatterns = [
    path('create/', CreateChannelView.as_view({
        'post': 'create',
    })),
    path('<int:pk>/update/', CreateChannelView.as_view({
        'put': 'update',
        'patch': 'partial_update',
    })),
    path('<int:pk>/subscriptions/', ChannelOwnerSubscriptionsView.as_view({
        'post': 'create',
        'get': 'list',
        'delete': 'destroy',
    })),
    path('', SearchChannelView.as_view({
        'get': 'list',
    })),
    path('<int:pk>/contents/', ChannelContentsView.as_view({
        'get': 'list',
    })),
]
