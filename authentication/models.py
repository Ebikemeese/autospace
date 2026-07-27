from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRole(models.TextChoices):
    CUSTOMER = 'CUSTOMER', 'Customer'
    MANAGER = 'MANAGER', 'Manager'
    VALET = 'VALET', 'Valet'
    ADMIN = 'ADMIN', 'Admin'

class User(AbstractUser):
    uid = models.CharField(max_length=255, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.CUSTOMER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'display_name']

    def __str__(self):
        return self.display_name or self.email or self.username

class Admin(models.Model):
    uid = models.CharField(max_length=255, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.display_name or self.uid
