from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    account_id = models.CharField(max_length=255, unique=True, null=True, blank=True)  # ID de Moov

    def deposit(self, amount):
        """Añadir dinero a la cuenta"""
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        """Retirar dinero"""
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False

class Transaction(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
