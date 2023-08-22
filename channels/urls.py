from django.urls import path

from channels.views import (
    ChannelOwnerSubscriptionsView,
    ChannelsView,
    SearchChannelView,
    CreateListContentsView,
    UpdateDestroyContentsView,
    ChannelAdminsView,
    ChannelSubscribersView,
)

urlpatterns = [
    path('create/', ChannelsView.as_view({
        'post': 'create',
    })),
    path('<int:pk>/', ChannelsView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    })),
    path('<int:channel_pk>/subscriptions/', ChannelOwnerSubscriptionsView.as_view({
        'post': 'create',
        'get': 'list',
        'delete': 'destroy',
    })),
    path('', SearchChannelView.as_view({
        'get': 'list',
    })),
    path('<int:channel_pk>/contents/', CreateListContentsView.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('contents/<int:pk>/', UpdateDestroyContentsView.as_view({
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
        'get': 'retrieve',
    })),
    path('<int:channel_pk>/admins/', ChannelAdminsView.as_view({
        'get': 'list',
    })),
    path('<int:channel_pk>/subscribers/', ChannelSubscribersView.as_view({
        'get': 'list',
    }))
]
