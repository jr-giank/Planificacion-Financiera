from django.urls import path
from .views import CreateAccountView, GetBalanceView, TransferMoneyView

urlpatterns = [
    path('create-account/', CreateAccountView.as_view(), name="create-account"),
    path('get-balance/', GetBalanceView.as_view(), name="get-balance"),
    path('transfer-money/', TransferMoneyView.as_view(), name="transfer-money"),
]