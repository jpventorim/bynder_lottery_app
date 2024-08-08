from __future__ import annotations

from datetime import UTC, date, datetime
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
    def validate_date_is_not_past(cls, game_date: datetime) -> datetime:
        today = datetime.now(tz=UTC)

        # Only the date is relevant for the comparison
        if game_date < today.date():
            raise ValueError("Date of the game cannot be in the past")
        return game_date

    # TODO: Validate date is not too far in the future. Maybe max of 1 week


class BallotOut(BallotIn):
    ballot_id: UUID4
    created_at: datetime


class WinningBallotOut(ModelSchema):
    winning_ballot: UUID4
    draw_date: PastDate

    class Meta:
        model = WinningBallots
        fields: ClassVar = ["winning_ballot", "draw_date"]
