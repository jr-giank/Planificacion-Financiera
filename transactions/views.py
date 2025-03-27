from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
import requests
import os

from moovio_sdk import Moov
from moovio_sdk.models import components

class CreateAccountView(APIView):
    """Crear una cuenta virtual en Moov y almacenarla localmente"""

    def post(self, request):
        user = request.user

        if not user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        if Account.objects.filter(user=user).exists():
            return Response({"message": "El usuario ya tiene una cuenta"}, status=status.HTTP_400_BAD_REQUEST)
        
        with Moov(
            security=components.Security(
                username=os.getenv('MV_PUBLIC_KEY'),
                password=os.getenv('MV_SECRET_KEY'),
            ),
        ) as moov:
            response = moov.accounts.create(account_type=components.AccountType.INDIVIDUAL, profile=components.CreateProfile(
                individual=components.CreateIndividualProfile(
                    name=components.IndividualName(
                        first_name=user.first_name,
                        last_name=user.last_name
                    ),
                    phone=components.PhoneNumber(
                        number=user.phone,
                        country_code="1",
                    ),
                    email=user.email,
                    birth_date=components.BirthDate(
                        day=user.birth_date.day,
                        month=user.birth_date.month,
                        year=user.birth_date.year,
                    ),
                ),
            ), mode=components.Mode.SANDBOX)
        
        if response:
            account = Account.objects.create(user=user, balance=0.00, account_id=response.result.account_id)
            return Response(AccountSerializer(account).data, status=status.HTTP_201_CREATED)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class GetBalanceView(APIView):
    """Obtener saldo de una cuenta"""

    def get(self, request):
        account = get_object_or_404(Account, user=request.user)
        return Response({"balance": account.balance})

class TransferMoneyView(APIView):
    """Realizar una transferencia entre cuentas"""

    pass
