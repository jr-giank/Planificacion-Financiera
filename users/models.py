from django.db import models
from django.contrib.auth.models import AbstractUser

class Addres(models.Model):
    
    address1 = models.CharField(max_length=255, null=False, blank=False)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=False, blank=False)
    state_or_province = models.CharField(max_length=100, null=False, blank=False)
    postal_code = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=50, null=False, blank=False)
    
    def __str__(self):
        return f"{self.address1} - {self.country}"

class BirthDate(models.Model):
    
    day = models.CharField(max_length=1, null=False, blank=False)
    month = models.CharField(max_length=10, null=False, blank=False)
    year = models.CharField(max_length=4, null=False, blank=False)

    def __str__(self):
        return f"{self.day}/{self.month}/{self.year}"

class User(AbstractUser):

    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.CharField(max_length=12, null=True, blank=True)
    password = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    username = models.CharField(max_length=70, unique=True, blank=True, null=True)
    address = models.ForeignKey(to=Addres, related_name='address', on_delete=models.SET_NULL, null=True, blank=True)
    birth_date = models.ForeignKey(to=BirthDate, related_name='birth_date', on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.username and self.email:
            self.username = self.email
        super(User, self).save(*args, **kwargs)