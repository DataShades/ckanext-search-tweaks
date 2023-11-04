from __future__ import annotations
from collections import defaultdict
from datetime import datetime, timedelta

from hashlib import md5
from typing import Any, Iterable, cast

from ckan.lib.redis import connect_to_redis
import ckan.plugins.toolkit as tk
from redis import Redis
from . import config

connect_to_redis: Any


class Score:
    redis: Redis[bytes]
    date_format = "%Y-%m-%d %H-%M"

    def __init__(self):
        self.redis = connect_to_redis()

        site = tk.config["ckan.site_id"]
        self.prefix = f"{site}:search_tweaks:qp"

    def save(self, q: str):
        q = q.strip()
        q_hash = md5(q.encode()).hexdigest()

        if self.is_throttling(q_hash):
            return

        self.redis.hset(self.trans_key(), q_hash, q)

        date_stem = self.format_date_stem(self.now())

        self.redis.hincrby(self.distribution_key(), f"{date_stem}/{q_hash}", 1)

    def is_throttling(self, q_hash: str):
        user = tk.current_user.name

        throttle_key = f"{self.prefix}:throttle:{user}:{q_hash}"
        if self.redis.exists(throttle_key):
            return True

        self.redis.set(throttle_key, 1, ex=config.throttle())
        return False

    def now(self):
        return datetime.utcnow()

    def score_key(self):
        return f"{self.prefix}:score"

    def trans_key(self):
        return f"{self.prefix}:trans"

    def distribution_key(self):
        return f"{self.prefix}:distribution"

    def format_date_stem(self, date: datetime):
        return date.strftime(self.date_format)

    def refresh(self):
        max_age = timedelta(seconds=config.max_age())
        dk = self.distribution_key()
        sk = self.score_key()

        expired_keys: set[bytes] = set()
        distribution = cast(
            "Iterable[tuple[bytes, bytes]]",
            self.redis.hscan_iter(dk),
        )

        scores: dict[bytes, float] = defaultdict(float)

        for k, v in distribution:
            date_str, q_hash = k.split(b"/", 1)
            date = datetime.strptime(date_str.decode(), self.date_format)
            age = self.now() - date

            if age > max_age:
                expired_keys.add(k)
                continue

            scores[q_hash] += int(v) / (age.days + 1)

        if expired_keys:
            self.redis.hdel(dk, *expired_keys)

        expired_keys: set[bytes] = set()
        for k, v in self.redis.zscan_iter(sk):
            if k not in scores:
                expired_keys.add(k)
                continue
        self.redis.zadd(sk, cast(Any, scores))

        if expired_keys:
            self.redis.zrem(sk, *expired_keys)

    def stats(self, num: int) -> Iterable[dict[str, Any]]:
        scores: list[tuple[bytes, float]] = self.redis.zrange(
            self.score_key(), 0, num - 1, desc=True, withscores=True
        )
        trans_key = self.trans_key()

        for k, v in scores:
            yield {"query": self.redis.hget(trans_key, k), "score": v}
