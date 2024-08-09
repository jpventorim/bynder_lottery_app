from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import TYPE_CHECKING

from ninja import Field, ModelSchema, Schema
from pydantic import UUID4, PastDate, field_validator

from games.models import WinningBallots


if TYPE_CHECKING:
    from typing import ClassVar


class BallotIn(Schema):
    game_date: date = Field(default_factory=datetime.now(tz=UTC).date)

    @field_validator("game_date")
    @classmethod
    def validate_game_date(cls, game_date: datetime) -> datetime:
        """Validate if game_date is not in the past or more than a week from today"""
        today = datetime.now(tz=UTC).date()

        # Only the date is relevant for the comparison
        if game_date < today:
            raise ValueError("Date of the game cannot be in the past")

        if game_date > today + timedelta(days=7):
            raise ValueError(
                "Date of the game cannot be more than one week in the future",
            )

        return game_date


class BallotOut(BallotIn):
    id: UUID4
    created_at: datetime


class WinningBallotOut(ModelSchema):
    winning_ballot_id: UUID4
    draw_date: PastDate

    class Meta:
        model = WinningBallots
        fields: ClassVar = ["winning_ballot_id", "draw_date"]
