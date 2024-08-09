from __future__ import annotations

from typing import ClassVar

from ninja import ModelSchema
from ninja.errors import HttpError
from pydantic import EmailStr, field_validator

from users.models import User


class UserCreateSchema(ModelSchema):
    username: str
    email: EmailStr

    class Meta:
        model = User
        fields: ClassVar = ["username", "email", "password", "first_name", "last_name"]

    @field_validator("username", mode="after")
    @classmethod
    def validate_unique_username(cls, username: str) -> str:
        if User.objects.filter(username=username).exists():
            raise HttpError(400, "Username already in use")
        return username
