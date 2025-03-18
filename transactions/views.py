from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
import requests
from requests.auth import HTTPBasicAuth
from .functions import get_moov_token

MOOV_BASE_URL = "https://api.moov.io"


class CreateAccountView(APIView):
    """Crear una cuenta virtual en Moov y almacenarla localmente"""

    def post(self, request):
        user = request.user

        if not user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        if Account.objects.filter(user=user).exists():
            return Response({"message": "El usuario ya tiene una cuenta"}, status=status.HTTP_400_BAD_REQUEST)

        access_token = get_moov_token()
        if not access_token:
            return Response({"error": "Failed to authenticate with Moov"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        data = {
            "accountType": "business",
            "profile": {
                "business": {
                    "legalBusinessName": "Whole Body Fitness LLC",
                    "businessType": "llc",
                    "website": "wbfllc.com"
                }
            },
            "foreignId": str(user.id)  # Unique identifier for your system
        }

        response = requests.post(f"{MOOV_BASE_URL}/accounts", json=data, headers=headers)

        print("Moov Response Status:", response.status_code)
        print("Moov Response Headers:", response.headers)
        print("Moov Response Content:", response.content.decode())  # Decode response bytes

        try:
            moov_data = response.json()  # Attempt to parse JSON
        except requests.exceptions.JSONDecodeError:
            return Response(
                {
                    "error": "Invalid JSON response from Moov",
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "content": response.content.decode()
                },
                status=response.status_code
            )
        
        if response.status_code == 201:
            moov_account_id = moov_data.get("id")
            account = Account.objects.create(user=user, balance=0.00, moov_account_id=moov_account_id)
            return Response(AccountSerializer(account).data, status=status.HTTP_201_CREATED)
        else:
            return Response(moov_data, status=response.status_code)

class GetBalanceView(APIView):
    """Obtener saldo de una cuenta"""

    def get(self, request):
        account = get_object_or_404(Account, user=request.user)
        return Response({"balance": account.balance})

class TransferMoneyView(APIView):
    """Realizar una transferencia entre cuentas"""

    def post(self, request):
        sender = get_object_or_404(Account, user=request.user)
        receiver_id = request.data.get("receiver_id")
        amount = request.data.get("amount")

        try:
            amount = float(amount)
        except ValueError:
            return Response({"message": "Monto inválido"}, status=status.HTTP_400_BAD_REQUEST)

        receiver = get_object_or_404(Account, id=receiver_id)

        # Simular la transferencia en Moov
        headers = {"Authorization": f"Bearer {MOOV_API_KEY}"}
        data = {
            "amount": {"currency": "USD", "value": str(amount)},
            "source": sender.moov_account_id,
            "destination": receiver.moov_account_id
        }

        response = requests.post(f"{MOOV_BASE_URL}/transfers", json=data, headers=headers)

        if response.status_code == 201:
            # Actualizar saldo localmente
            if sender.withdraw(amount):
                receiver.deposit(amount)
                Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)
                return Response({"message": "Transferencia realizada"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Fondos insuficientes"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response.json(), status=response.status_code)
