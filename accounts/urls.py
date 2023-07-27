from django.urls import path

from accounts.views import GhasedLoginView, GhasedSignUpView, GhasedProfileView

urlpatterns = [
    path('login/', GhasedLoginView.as_view()),
    path('signup/', GhasedSignUpView.as_view()),
    path('profile/', GhasedProfileView.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
    })),
]
