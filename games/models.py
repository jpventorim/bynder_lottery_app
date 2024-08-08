from __future__ import annotations

import uuid
from datetime import datetime

from django.db import models


class LotteryBallots(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="ballots",
    )
    game_date = models.DateField(default=datetime.today)
    is_winner = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class WinningBallots(models.Model):
    winning_ballot = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    draw_date = models.DateField(default=datetime.today)
