from __future__ import annotations

from django.http import HttpRequest

from users.models import User


class AuthenticatedHttpRequest(HttpRequest):
    """This is to ensure the request user is not AnonymousUser type"""

    user: User
