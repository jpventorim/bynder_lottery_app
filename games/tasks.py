from __future__ import annotations

import secrets
from datetime import UTC, date, datetime, timedelta

from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction

from games.lottery_draw_helpers import get_list_of_ballot_ids, report_winning_ballot


logger = get_task_logger(__name__)


@shared_task(
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 10, "countdown": 60},
)
def lottery_draw() -> None:
    with transaction.atomic():
        # Uses the previous day
        game_date: date = datetime.now(tz=UTC).date() - timedelta(days=1)

        ballots = get_list_of_ballot_ids(game_date=game_date)
        if ballots:
            winning_ballot = secrets.choice(ballots)
            report_winning_ballot(winning_ballot)
            logger.info(f"Lottery Winner id: {winning_ballot}. Game on {game_date}")
        else:
            logger.warning(f"No ballots found for game on: {game_date}")
