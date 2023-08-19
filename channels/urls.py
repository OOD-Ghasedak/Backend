from django.urls import path

from channels.views import (
    ChannelOwnerSubscriptionsView,
    CreateChannelView,
    SearchChannelView,
    CreateListContentsView,
    UpdateRetrieveContentsView,
    CreateContentFileView,
    UpdateContentFileView,
)

urlpatterns = [
    path('create/', CreateChannelView.as_view({
        'post': 'create',
    })),
    path('<int:pk>/update/', CreateChannelView.as_view({
        'put': 'update',
        'patch': 'partial_update',
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
    path('contents/<int:pk>/', UpdateRetrieveContentsView.as_view({
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('contents/<int:content_pk>/files/', CreateContentFileView.as_view({
        'post': 'create',
        'get': 'retrieve'
    })),
    path('contents/files/<int:pk>/', UpdateContentFileView.as_view({
        'put': 'update',
        'delete': 'destroy',
    })),
]
