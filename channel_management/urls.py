from django.urls import path

from channel_management.views import ManagedChannelsView, CreateAdminsView, DestroyUpdateAdminsView

urlpatterns = [
    path('managed-channels/', ManagedChannelsView.as_view()),
    path('<int:channel_pk>/admins/', CreateAdminsView.as_view({'post': 'create'})),
    path('admins/<int:pk>/', DestroyUpdateAdminsView.as_view({
        'delete': 'destroy',
        'put': 'update',
        'patch': 'partial_update',
    })),
]
