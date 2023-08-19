from django.urls import path

from subscribe.views import SubscribedChannelsView

urlpatterns = [
    path('joined-channels/', SubscribedChannelsView.as_view()),
]
