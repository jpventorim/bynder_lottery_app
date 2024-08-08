from __future__ import annotations

from django.contrib import admin
from django.urls import re_path
from ninja import NinjaAPI
from ninja.throttling import AnonRateThrottle, AuthRateThrottle
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.routers.obtain import obtain_pair_router
from ninja_jwt.routers.verify import verify_router


api = NinjaAPI(
    title="Lottery API",
    description="Lottery API to submit and check results of lottery games",
    auth=JWTAuth(),
    throttle=[
        AnonRateThrottle("10/s"),
        AuthRateThrottle("100/s"),
    ],
)
from django.urls import path
api.add_router("/lottery", "games.views.router")

# JWT Auth routers
api.add_router("/token", tags=["Auth"], router=obtain_pair_router)
api.add_router("/token", tags=["Auth"], router=verify_router)


urlpatterns = [
    re_path(r"^", api.urls),
    re_path(r"^admin/", admin.site.urls),
]
