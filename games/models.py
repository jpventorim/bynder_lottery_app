from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from django.db import models


if TYPE_CHECKING:
    from typing import ClassVar


class LotteryBallots(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="ballots",
    )
    game_date = models.DateField(default=datetime.today)
    is_winner = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()


class WinningBallots(models.Model):
    winning_ballot_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    draw_date = models.DateField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        # Index draw_date in descending order
        # as the most recent games should be queried more often
        indexes: ClassVar = [
            models.Index(
                name="draw_date_descending",
                fields=["-draw_date"],
            ),
        ]
