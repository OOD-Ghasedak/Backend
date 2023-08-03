from django.urls import path

from channels.views import ChannelOwnerSubscriptionsView
from channels.views.channels import CreateChannelView

urlpatterns = [
    path('create/', CreateChannelView.as_view({
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
    })),
    path('update/<int:pk>/', CreateChannelView.as_view({
        'put': 'update',
        'patch': 'partial_update',
    })),
    path('<int:pk>/subscriptions/', ChannelOwnerSubscriptionsView.as_view({
        'post': 'create',
        'get': 'list',
        'delete': 'destroy',
    })),
]
