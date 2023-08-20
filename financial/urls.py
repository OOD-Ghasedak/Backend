from django.urls import path

from financial.views import WalletView, DepositView, WithdrawView

urlpatterns = [
    path('wallet/', WalletView.as_view()),
    path('deposit/', DepositView.as_view({
        'post': 'create'
    })),
    path('withdraw/', WithdrawView.as_view({
        'post': 'create'
    })),
]
