from django.urls import path

from accounts.view import GhasedLoginView, GhasedSignUpView

urlpatterns = [
    path('login/', GhasedLoginView.as_view()),
    path('signup/', GhasedSignUpView.as_view()),
]
