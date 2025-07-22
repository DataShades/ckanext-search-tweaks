from __future__ import annotations

import logging
from typing import Any
from collections.abc import Iterable

from ckanext.toolbelt.utils.tracking import DateTracker

from . import config

log = logging.getLogger(__name__)
connect_to_redis: Any


class Score:
    def __init__(self):
        self.track = DateTracker(
            "search_tweaks:qp",
            throttling_time=config.throttle(),
            max_age=config.max_age(),
            obsoletion_period=config.obsoletion_period(),
            personalized=True,
        )

    def export(self):
        return self.track.snapshot()

    def restore(self, snapshot: Any):
        return self.track.restore(snapshot)

    def hit(self, q: str):
        self.track.hit(q)

    def refresh(self):
        self.track.refresh()

    def stats(self, num: int) -> Iterable[dict[str, str | float]]:
        return self.track.most_common(num)

    def drop(self, q: str):
        self.track.drop(q)

    def reset(self):
        self.track.reset()

    def ignore(self, q: str):
        self.track.ignore(self.track.hash(q))
