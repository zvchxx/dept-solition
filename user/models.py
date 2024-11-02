from django.db import models

from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    phonenumber = models.CharField(max_length=20)