from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class TargetProperty(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()

    def __str__(self):
        return self.name

class SavingGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField()

    def __str__(self):
        return f"Saving Goal for {self.user.name}: {self.target_amount}"

class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(SavingGoal, on_delete=models.CASCADE)
    amount_invested = models.DecimalField(max_digits=10, decimal_places=2)
    expected_return = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()

    def __str__(self):
        return f"Investment of {self.amount_invested} by {self.user.name}"
