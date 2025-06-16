from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=[
        ('Superadmin', 'СуперАдмин'),
        ('Teacher', 'Учитель'),
        ('Accountant', 'Бухгалтер'),
        ('Manager', 'Мэнеджер'),
    ], default='Teacher')
