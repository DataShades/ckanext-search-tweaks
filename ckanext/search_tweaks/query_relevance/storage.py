from __future__ import annotations
from abc import ABC, abstractclassmethod, abstractmethod
from datetime import date, timedelta
from typing import Any, Iterable, Optional, cast, Tuple

import ckan.plugins.toolkit as tk
from ckan.lib.redis import connect_to_redis, Redis

CONFIG_DAILY_AGE = "ckanext.search_tweaks.query_relevance.daily.age"
DEFAULT_DAILY_AGE = 90

ScanItem = Tuple[str, str, int]


class ScoreStorage(ABC):
    id: str
    query: str

    def __init__(self, id_: str, query: str):
        self.id = id_
        self.query = query

    @abstractmethod
    def get(self) -> int:
        """Get current value."""
        ...

    @abstractmethod
    def inc(self, by: int) -> None:
        """Increase current value by the given value."""
        ...

    @abstractmethod
    def set(self, value: int) -> None:
        """Replace current value with the given one."""
        ...

    @classmethod
    @abstractclassmethod
    def scan(cls, id_: Optional[str] = None) -> Iterable[ScanItem]:
        """Get all the scores."""
        ...

    @classmethod
    @abstractclassmethod
    def reset_storage(cls):
        """Remove everything from storage."""
        ...

    def reset(self) -> None:
        """Set current value to zero."""
        self.set(0)

    def align(self) -> None:
        """Make some cleanup in order to maintain fast and correct value."""
        pass


class RedisScoreStorage(ScoreStorage):
    _conn: Optional[Redis] = None

    @property
    def conn(self):
        if not self._conn:
            self._conn = self.connect()
        return self._conn

    @staticmethod
    def connect():
        return connect_to_redis()

    @staticmethod
    def _common_key_part() -> str:
        site_id = tk.config["ckan.site_id"]  # type: ignore
        return f"{site_id}:land:query_scores"

    @classmethod
    def reset_storage(cls):
        conn = cls.connect()
        for key in conn.keys(f"{cls._common_key_part()}:*"):
            conn.delete(key)

    @abstractmethod
    def _key(self) -> str:
        ...

    def reset(self):
        self.conn.delete(self._key())


class PermanentRedisScoreStorage(RedisScoreStorage):
    """Put all the points into the same cell.

    Sparingly uses memory and must be prefered when there are no extra
    requirements for invalidation of stats.

    """

    def set(self, value: int) -> None:
        self.conn.hset(self._key(), self.query, value)

    def get(self) -> int:
        return int(self.conn.hget(self._key(), self.query) or 0)

    def inc(self, by: int) -> None:
        self.conn.hincrby(self._key(), self.query, by)

    def _key(self):
        return f"{self._common_key_part()}:{self.id}"

    @classmethod
    def scan(cls, id_: Optional[str] = None) -> Iterable[ScanItem]:
        conn = cls.connect()
        common_key = cls._common_key_part()
        if id_:
            pattern = f"{common_key}:{id_}"
        else:
            pattern = f"{common_key}:*"
        for key in conn.keys(pattern):
            _, row_id = key.rsplit(b":", 1)
            for query, score in conn.hgetall(key).items():
                yield row_id.decode(), query.decode(), int(score)


class DailyRedisScoreStorage(RedisScoreStorage):
    """Store data inside different cells depending on current date.

    The longer index exists, the more memory it consumes. But it can be aligned
    periodically in order to free memory.

    """

    def set(self, value: int) -> None:
        key = self._key()
        zkey = self._zkey()

        self.conn.zadd(key, {zkey: value})

    def get(self) -> int:
        key = self._key()
        values = self.conn.zrange(key, 0, -1, withscores=True)
        total = self._total(values)
        return total

    @staticmethod
    def _total(values: list[tuple[Any, Any]]) -> int:
        return int(sum(map(lambda pair: cast(float, pair[1]), values)))

    def inc(self, by: int) -> None:
        key = self._key()
        zkey = self._zkey()
        # type-stubs don't know that signature is (key, amount, value)
        self.conn.zincrby(key, by, zkey)  # type: ignore

    def align(self):
        age = tk.asint(tk.config.get(CONFIG_DAILY_AGE, DEFAULT_DAILY_AGE))
        verge = bytes((date.today() - timedelta(days=age)).isoformat(), "utf8")
        key = self._key()

        for day in self.conn.zrange(key, 0, -1):
            if day >= verge:
                continue
            self.conn.zrem(key, day)

    def _key(self) -> str:
        return f"{self._common_key_part()}:{self.id}:{self.query}"

    def _zkey(self):
        return date.today().isoformat()

    @classmethod
    def scan(cls, id_: Optional[str] = None) -> Iterable[ScanItem]:
        conn = cls.connect()
        common_key = cls._common_key_part()
        if id_:
            pattern = f"{common_key}:{id_}:*"
        else:
            pattern = f"{common_key}:*"
        for key in conn.keys(pattern):
            _, id_, query = key.decode().rsplit(":", 2)
            yield id_, query, cls(id_, query).get()
