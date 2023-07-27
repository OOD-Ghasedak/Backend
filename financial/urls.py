from django.urls import path

from financial.views import WalletView

urlpatterns = [
    path('wallet/', WalletView.as_view()),
]
