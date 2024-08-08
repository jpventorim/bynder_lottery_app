from __future__ import annotations

from typing import ClassVar

from ninja import ModelSchema
from ninja.errors import HttpError
from pydantic import EmailStr, field_validator

from users.models import User


class UserCreateSchema(ModelSchema):
    email: EmailStr

    class Meta:
        model = User
        fields: ClassVar = ["email", "password", "first_name", "last_name"]

    @field_validator("email", mode="after")
    @classmethod
    def validate_unique_email(cls, email_value: EmailStr) -> EmailStr:
        if User.objects.filter(email=email_value).exists():
            raise HttpError(400, "Email already in use")
        return email_value
