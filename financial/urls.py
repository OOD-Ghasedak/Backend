from django.urls import path

from financial.views import WalletView, DepositView

urlpatterns = [
    path('wallet/', WalletView.as_view()),
    path('deposit/', DepositView.as_view({
        'post': 'create'
    })),
    path('withdraw/', DepositView.as_view({
        'post': 'create'
    })),
]
