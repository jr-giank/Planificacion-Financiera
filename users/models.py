from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=70, unique=True, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name']

    def save(self, *args, **kwargs):
        if not self.username and self.email:
            self.username = self.email
        super(User, self).save(*args, **kwargs)