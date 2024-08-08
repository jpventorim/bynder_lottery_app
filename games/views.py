from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from pydantic import PastDate

from games.models import LotteryBallots, WinningBallots
from games.schemas import BallotIn, BallotOut, WinningBallotOut


if TYPE_CHECKING:
    from users.models import User


router = Router(tags=["Lottery Ballots"])


@router.post(
    "/submit_ballot",
    response={201: BallotOut},
    url_name="submit_ballot",
    description="Allows user to submit one ballot to a lottery game within the next week",
)
def post_submit_ballot(
    request: HttpRequest,
    payload: BallotIn,
) -> tuple[int, LotteryBallots]:
    user: User = request.user
    ballot = LotteryBallots.objects.create(user=user, game_date=payload.game_date)

    return 201, ballot


@router.get(
    "/winning_ballot",
    response={200: WinningBallotOut},
    url_name="winning_ballot",
    description="Allows user to fetch winning ballot of a specified date",
)
def get_winning_ballot(
    request: HttpRequest,
    draw_date: PastDate,
) -> tuple[int, WinningBallots]:
    winning_ballot = get_object_or_404(WinningBallots, draw_date=draw_date)

    return 200, winning_ballot
