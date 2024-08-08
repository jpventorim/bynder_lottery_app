from __future__ import annotations

import uuid
from typing import ClassVar

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, email, password, **extra_fields) -> User:
        """
        Create and save a user with the given email, and password.
        """
        email = self.normalize_email(email)
        user: User = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save()
        return user


class User(AbstractUser):
    # We use email as username instead
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar = []

    objects = CustomUserManager()
