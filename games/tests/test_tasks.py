from __future__ import annotations

import logging
from datetime import date, timedelta

from pytest import LogCaptureFixture

from games.models import LotteryBallots, WinningBallots
from games.tasks import lottery_draw
from users.models import User


LOGGER = logging.getLogger(__name__)


def test_lottery_draw__no_games_found(caplog: LogCaptureFixture, today: date) -> None:
    yesterday = today - timedelta(days=1)
    with caplog.at_level(logging.WARNING):
        lottery_draw()

    assert f"No ballots found for game on: {yesterday}" in caplog.text


def test_lottery_draw__winner_found(
    caplog: LogCaptureFixture,
    user: User,
    today: date,
) -> None:
    yesterday = today - timedelta(days=1)
    single_ballot = LotteryBallots.objects.create(user=user, game_date=yesterday)

    with caplog.at_level(logging.INFO):
        lottery_draw()

    assert f"Lottery Winner id: {single_ballot.pk!s}. Game on {yesterday}" in caplog.text
    assert WinningBallots.objects.get(pk=single_ballot.pk)
    single_ballot.refresh_from_db()
    assert single_ballot.is_winner is True


def test_lottery_draw__multiple_ballots(user: User, today: date) -> None:
    yesterday = today - timedelta(days=1)
    yesterday_ballots = [LotteryBallots(user=user, game_date=yesterday) for _ in range(5)]
    LotteryBallots.objects.bulk_create(yesterday_ballots)

    assert WinningBallots.objects.count() == 0
    assert LotteryBallots.objects.filter(is_winner=True).count() == 0
    lottery_draw()

    assert WinningBallots.objects.count() == 1
    assert LotteryBallots.objects.filter(is_winner=True).count() == 1
