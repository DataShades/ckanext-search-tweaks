from __future__ import annotations
from collections import defaultdict
from datetime import datetime, timedelta
import logging
from hashlib import md5
from typing import Any, Iterable, cast
from operator import itemgetter
from ckan.lib.redis import connect_to_redis
import ckan.plugins.toolkit as tk
from redis import Redis
from . import config

log = logging.getLogger(__name__)
connect_to_redis: Any


class Score:
    redis: Redis[bytes]
    date_format = "%Y-%m-%d %H-%M"

    def __init__(self):
        self.redis = connect_to_redis()

        site = tk.config["ckan.site_id"]
        self.prefix = f"{site}:search_tweaks:qp"

    def export(self):
        data: dict[bytes, dict[str, Any]] = {
            hash: {"query": query, "records": []}
            for hash, query in self.redis.hgetall(self.trans_key()).items()
        }
        for k, v in self.redis.hscan_iter(self.distribution_key()):
            date_str, q_hash = k.split(b"/", 1)
            try:
                date = datetime.strptime(date_str.decode(), self.date_format)
            except ValueError:
                continue

            data[q_hash]["records"].append({"date": date, "count": int(v)})

        return list(data.values())

    def save(self, q: str):
        q = q.strip()
        q_hash = self.hash(q)

        if self.is_ignored(q_hash):
            return

        if self.is_throttling(q_hash):
            return

        self.redis.hset(self.trans_key(), q_hash, q)

        date_stem = self.format_date_stem(self.now())

        self.redis.hincrby(self.distribution_key(), f"{date_stem}/{q_hash}", 1)

    def drop(self, q: str):
        q_hash = self.hash(q)
        dk = self.distribution_key()

        series = self.redis.hscan_iter(dk, f"*/{q_hash}")
        keys = list(map(itemgetter(0), series))
        if keys:
            self.redis.hdel(dk, *keys)

        self.redis.hdel(self.trans_key(), q_hash)
        self.redis.zrem(self.score_key(), q_hash)

    def is_throttling(self, q_hash: str):
        user = tk.current_user.name

        throttle_key = f"{self.prefix}:throttle:{user}:{q_hash}"
        if self.redis.exists(throttle_key):
            return True

        self.redis.set(throttle_key, 1, ex=config.throttle())
        return False

    def reset(self):
        keys = self.redis.keys(f"{self.prefix}:*")
        if keys:
            self.redis.delete(*keys)

    def refresh(self):
        max_age = timedelta(seconds=config.max_age())
        dk = self.distribution_key()
        sk = self.score_key()

        expired_dist: set[bytes] = set()
        distribution = cast(
            "Iterable[tuple[bytes, bytes]]",
            self.redis.hscan_iter(dk),
        )

        scores: dict[bytes, float] = defaultdict(float)

        for k, v in distribution:
            date_str, q_hash = k.split(b"/", 1)
            try:
                date = datetime.strptime(date_str.decode(), self.date_format)
            except ValueError:
                log.error("Remove invalid key %s", k)
                expired_dist.add(k)
                continue

            age = self.now() - date

            if age > max_age:
                expired_dist.add(k)
                continue

            scores[q_hash] += int(v) / (age.seconds // config.obsoletion_period() + 1)

        if expired_dist:
            self.redis.hdel(dk, *expired_dist)

        expired_scores: set[bytes] = set()
        for k, v in self.redis.zscan_iter(sk):
            if k not in scores:
                expired_scores.add(k)
                continue
        if scores:
            self.redis.zadd(sk, cast(Any, scores))

        if expired_scores:
            self.redis.zrem(sk, *expired_scores)
            self.redis.hdel(self.trans_key(), *expired_scores)

    def hash(self, q: str):
        return md5(q.encode()).hexdigest()

    def is_ignored(self, q_hash: str):
        return self.redis.sismember(self.ignore_key(), q_hash)

    def ignore(self, q: str):
        return self.redis.sadd(self.ignore_key(), self.hash(q))

    def now(self):
        return datetime.utcnow()

    def score_key(self):
        return f"{self.prefix}:score"

    def trans_key(self):
        return f"{self.prefix}:trans"

    def ignore_key(self):
        return f"{self.prefix}:ignore"

    def distribution_key(self):
        return f"{self.prefix}:distribution"

    def format_date_stem(self, date: datetime):
        return date.strftime(self.date_format)

    def stats(self, num: int) -> Iterable[dict[str, Any]]:
        scores: list[tuple[bytes, float]] = self.redis.zrange(
            self.score_key(), 0, num - 1, desc=True, withscores=True
        )
        trans_key = self.trans_key()

        for k, v in scores:
            yield {"query": self.redis.hget(trans_key, k), "score": v}
