from django.urls import path

from channels.views.create_channel import CreateChannelView

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
]
