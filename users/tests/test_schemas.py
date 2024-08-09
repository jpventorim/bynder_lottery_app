from __future__ import annotations

import pytest
from ninja.errors import HttpError

from users.models import User
from users.schemas import UserCreateSchema


def test_user_create_schema__existing_username(user: User) -> None:
    existing_username = user.username

    with pytest.raises(HttpError) as exc_info:
        UserCreateSchema(
            username=existing_username,
            email="foo@bar.com",
            password="very_safe",
            first_name="first_name",
            last_name="last_name",
        )

    assert exc_info.type is HttpError
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == "Username already in use"
