from django.db import models
from django.contrib.auth.models import AbstractUser

from role_management.models import Role

# Create your models here.

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
