from __future__ import annotations

from django.http import HttpRequest
from ninja import Router

from users.models import User
from users.schemas import UserCreateSchema


router = Router(tags=["Users"])


@router.post(
    "/register",
    response={204: None},
    url_name="register",
    auth=None,
    description="Registers a new user with email and password",
)
def post_user_register(
    request: HttpRequest,
    payload: UserCreateSchema,
) -> tuple[int, None]:
    User.objects.create_user(**payload.model_dump())

    return 204, None
