from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

from django.test import Client
from django.urls import reverse
from freezegun import freeze_time

from games.models import WinningBallots


def test_post_submit_ballot__valid_date(
    logged_client: Client,
    today: date,
    api_auth_header: dict[str, str],
) -> None:
    url = reverse("lottery:submit_ballot")
    payload = {"game_date": today}

    response = logged_client.post(
        url,
        data=payload,
        content_type="application/json",
        headers=api_auth_header,
    )

    assert response.status_code == 201
    resp_body = response.json()
    assert resp_body["id"]
    assert str(today) in resp_body["created_at"]


def test_post_submit_ballot__past_date_fails(
    logged_client: Client,
    today: date,
    api_auth_header: dict[str, str],
) -> None:
    game_date = today - timedelta(days=1)
    url = reverse("lottery:submit_ballot")
    payload = {"game_date": game_date}

    response = logged_client.post(
        url,
        data=payload,
        content_type="application/json",
        headers=api_auth_header,
    )

    assert response.status_code == 422
    resp_body = response.json()["detail"][0]
    assert resp_body["type"] == "value_error"
    assert resp_body["loc"] == ["body", "payload", "game_date"]
    assert resp_body["msg"] == "Value error, Date of the game cannot be in the past"


def test_post_submit_ballot__unauthorized(logged_client: Client, today: date) -> None:
    url = reverse("lottery:submit_ballot")
    payload = {"game_date": today}

    response = logged_client.post(
        url,
        data=payload,
        content_type="application/json",
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_get_winning_ballot(
    logged_client: Client,
    api_auth_header: dict[str, str],
) -> None:
    url = reverse("lottery:winning_ballot")

    with freeze_time(datetime.now(tz=UTC) - timedelta(days=1)):
        draw_date = str(datetime.now(tz=UTC).date())
        WinningBallots.objects.create()

    response = logged_client.get(
        url,
        data={"draw_date": draw_date},
        headers=api_auth_header,
    )

    assert response.status_code == 200
    resp_body = response.json()
    assert resp_body["winning_ballot_id"]
    assert resp_body["draw_date"] == draw_date


def test_get_winning_ballot__not_found(
    logged_client: Client,
    api_auth_header: dict[str, str],
    today: date,
) -> None:
    url = reverse("lottery:winning_ballot")
    draw_date = str(today - timedelta(days=1))

    response = logged_client.get(
        url,
        data={"draw_date": draw_date},
        content_type="application/json",
        headers=api_auth_header,
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_get_winning_ballot__future_date_fails(
    logged_client: Client,
    api_auth_header: dict[str, str],
    today: date,
) -> None:
    url = reverse("lottery:winning_ballot")
    response = logged_client.get(
        url,
        data={"draw_date": str(today)},
        content_type="application/json",
        headers=api_auth_header,
    )

    assert response.status_code == 422
    resp_body = response.json()["detail"][0]
    assert resp_body["type"] == "date_past"
    assert resp_body["loc"] == ["query", "draw_date"]
    assert resp_body["msg"] == "Date should be in the past"


def test_get_winning_ballot__unauthorized(logged_client: Client) -> None:
    url = reverse("lottery:winning_ballot")

    with freeze_time(datetime.now(tz=UTC) - timedelta(days=1)):
        draw_date = str(datetime.now(tz=UTC).date())
        WinningBallots.objects.create()

    response = logged_client.get(url, data={"draw_date": draw_date})

    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}
