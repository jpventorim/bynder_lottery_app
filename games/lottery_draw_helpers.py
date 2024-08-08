from __future__ import annotations

from datetime import date

from pydantic import UUID4

from games.models import LotteryBallots, WinningBallots


def get_list_of_ballot_ids(game_date: date) -> list[UUID4]:
    """Retrieves a list of ballot ids for a specific date"""

    # Make sure `is_winner` is false so it can support multiple drawings in one day
    return LotteryBallots.objects.filter(
        game_date=game_date,
        is_winner=False,
    ).values_list("id", flat=True)


def report_winning_ballot(winning_ballot_id: UUID4) -> None:
    """Creates an entry in WinningBallots with the ballot id and set ballot as winner"""

    LotteryBallots.objects.filter(id=winning_ballot_id).update(is_winner=True)
    WinningBallots.objects.create(winning_ballot_id=winning_ballot_id)
