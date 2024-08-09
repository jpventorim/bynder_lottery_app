from __future__ import annotations

from datetime import date, timedelta

import pytest

from games.lottery_draw_helpers import get_list_of_ballot_ids, report_winning_ballot
from games.models import LotteryBallots, WinningBallots
from users.models import User


@pytest.fixture
def day_with_ballots(user: User, today: date) -> list[LotteryBallots]:
    new_ballots = [LotteryBallots(user=user, game_date=today) for _ in range(5)]
    return LotteryBallots.objects.bulk_create(new_ballots)


def test_get_list_of_ballot_ids__returns_list(
    day_with_ballots: list[LotteryBallots], today: date,
) -> None:
    ids_list = get_list_of_ballot_ids(game_date=today)

    assert len(day_with_ballots) == len(ids_list)
    for ballot in day_with_ballots:
        assert ballot.pk in ids_list


def test_get_list_of_ballot_ids__empty_day(today: date) -> None:
    game_date = today + timedelta(days=5)

    assert not LotteryBallots.objects.filter(game_date=game_date).exists()

    ids_list = get_list_of_ballot_ids(game_date=game_date)
    assert not ids_list


def test_report_winning_ballot__report_created(
    day_with_ballots: list[LotteryBallots], today: date,
) -> None:
    winning_ballot = LotteryBallots.objects.first()
    assert winning_ballot

    report_winning_ballot(winning_ballot_id=winning_ballot.pk)

    assert LotteryBallots.objects.get(pk=winning_ballot.pk).is_winner is True
    report = WinningBallots.objects.get(pk=winning_ballot.pk)
    assert report.pk == winning_ballot.pk
    assert report.draw_date == today
