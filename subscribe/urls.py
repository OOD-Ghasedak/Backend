from django.urls import path

from accounts.views import GhasedLoginView

urlpatterns = [
    path('joined-channels/', GhasedLoginView.as_view()),
]
