from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from games.schemas import BallotIn


def test_ballot_in_validate_game_date__within_range() -> None:
    game_date = datetime.now(tz=UTC).date()

    schema = BallotIn(game_date=game_date)
    assert schema


def test_ballot_in_validate_game_date__past_date_fails() -> None:
    game_date = datetime.now(tz=UTC).date() - timedelta(days=1)

    with pytest.raises(ValidationError) as exc_info:
        BallotIn(game_date=game_date)

    assert exc_info.type is ValidationError
    errors = exc_info.value.errors()

    assert errors[0]["loc"] == ("game_date",)
    assert errors[0]["msg"] == "Value error, Date of the game cannot be in the past"
    assert errors[0]["input"] == game_date


def test_ballot_in_validate_game_date__more_than_a_week_fails() -> None:
    game_date = datetime.now(tz=UTC).date() + timedelta(days=8)

    with pytest.raises(ValidationError) as exc_info:
        BallotIn(game_date=game_date)

    assert exc_info.type is ValidationError
    errors = exc_info.value.errors()

    assert errors[0]["loc"] == ("game_date",)
    assert (
        errors[0]["msg"]
        == "Value error, Date of the game cannot be more than one week in the future"
    )
    assert errors[0]["input"] == game_date
