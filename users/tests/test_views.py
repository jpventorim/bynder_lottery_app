from __future__ import annotations

from django.test import Client
from django.urls import reverse

from users.models import User


def test_post_user_register(client: Client) -> None:
    url = reverse("lottery:register")
    payload = {
        "username": "cool_username",
        "email": "new_email@example.com",
        "password": "also_safe",
        "first_name": "First",
        "last_name": "Last",
    }
    response = client.post(url, data=payload, content_type="application/json")

    assert response.status_code == 204
    user = User.objects.get(username=payload["username"])
    assert user.username == payload["username"]
    assert user.email == payload["email"]
    assert user.first_name == payload["first_name"]
    assert user.last_name == payload["last_name"]


def test_post_user_register__existing_username(client: Client, user: User) -> None:
    url = reverse("lottery:register")
    payload = {
        "username": user.username,
        "email": "new_email@example.com",
        "password": "also_safe",
        "first_name": "First",
        "last_name": "Last",
    }
    response = client.post(url, data=payload, content_type="application/json")

    assert response.status_code == 400
    assert response.json() == {"detail": "Username already in use"}
