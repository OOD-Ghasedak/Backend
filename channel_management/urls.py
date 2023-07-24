from django.urls import path

from channel_management.views import ManagedChannelsView

urlpatterns = [
    path('managed-channels/', ManagedChannelsView.as_view()),
]
