from __future__ import annotations

import os
from datetime import UTC, date, datetime

import pytest
from django.test.client import Client
from django.urls import reverse

from users.models import User


os.environ["RUNNING_TESTS"] = "True"


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def user() -> User:
    username = "user_test"
    password = "test_pass"  # noqa: S105
    email = "testing@tests.com"
    first_name = "first_name"
    last_name = "last_name"

    return User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )


@pytest.fixture
def api_auth_header(client: Client, user: User) -> dict[str, str]:
    url = reverse("lottery:token_obtain_pair")
    payload = {"username": user.username, "password": "test_pass"}
    response = client.post(url, data=payload, content_type="application/json")
    return {"Authorization": f"Bearer {response.json()["access"]}"}


@pytest.fixture
def logged_client(client: Client, user: User) -> Client:
    client.login(username=user.username, password=user.password)
    return client


@pytest.fixture
def today() -> date:
    return datetime.now(tz=UTC).date()
