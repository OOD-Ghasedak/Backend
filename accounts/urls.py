from django.urls import path

from accounts.views import (
    GhasedLoginView,
    GhasedSignUpView,
    GhasedProfileView,
    VerifyForRegisterView,
    ChangePasswordView,
)

urlpatterns = [
    path('login/', GhasedLoginView.as_view()),
    path('signup/', GhasedSignUpView.as_view()),
    path('verify-signup/', VerifyForRegisterView.as_view({
        'post': 'create'
    })),
    path('profile/', GhasedProfileView.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
    })),
    path('change-password/', ChangePasswordView.as_view())
]
