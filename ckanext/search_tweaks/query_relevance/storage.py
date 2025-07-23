from __future__ import annotations

from ckan.lib.redis import connect_to_redis


ScanItem = tuple[str, int]


class QueryHitTracker:
    def __init__(self, entity_id: str, query: str, ttl: int | None = None):
        self.entity_id = entity_id
        self.query = query
        self.conn = self.make_connection()
        self.ttl = ttl

    @classmethod
    def make_connection(cls):
        return connect_to_redis()

    @classmethod
    def _key(cls, query: str) -> str:
        return f"search-tweaks:query-relevance:{query}"

    def increase(self, amount: int) -> None:
        """Increase the score for the specific entity_id + query.

        Args:
            amount: amount to increase the score by
        """
        key = self._key(self.query)
        pipe = self.conn.pipeline()

        pipe.zincrby(key, amount, self.entity_id)

        if self.ttl is not None:
            pipe.expire(key, self.ttl)

        pipe.execute()

    def get(self) -> int | None:
        """Get the score for the specific entity_id + query.

        Returns:
            score or None if not found
        """
        result = self.conn.zscore(self._key(self.query), self.entity_id)
        return int(result) if result else 0  # type: ignore

    @classmethod
    def get_all(cls) -> list[tuple[str, str, int]]:
        """Get all scores.

        Returns:
            list of (entity_id, query, score) tuples
        """
        conn = cls.make_connection()
        cursor = 0
        results: list[tuple[str, str, int]] = []

        while True:
            cursor, keys = conn.scan(cursor=cursor, match=cls._key("*"), count=1000)  # type: ignore

            for key in keys:
                query = key.decode().rsplit(":", 1)[-1]

                for entity_id, score in conn.zrange(key, 0, -1, withscores=True):  # type: ignore
                    results.append((entity_id.decode(), query, int(score)))

            if cursor == 0:
                break

        return results

    @classmethod
    def top(cls, query: str, limit: int = 100) -> list[tuple[bytes, float]]:
        """Return the top N entities for the given query.

        Args:
            query: search query
            limit (optional): maximum number of entities to return

        Returns:
            list of (entity_id, score) tuples
        """
        conn = cls.make_connection()

        return conn.zrevrange(  # type: ignore
            cls._key(query),
            0,
            limit - 1,
            withscores=True,
        )

    @classmethod
    def reset(cls, query: str) -> None:
        """Reset scores for the given query.

        Args:
            query: search query
        """
        cls.make_connection().delete(cls._key(query))

    @classmethod
    def reset_all(cls) -> None:
        """Reset all scores."""
        cursor = 0
        conn = cls.make_connection()

        while True:
            cursor, keys = conn.scan(cursor=cursor, match=cls._key("*"), count=1000)  # type: ignore

            if keys:
                conn.delete(*keys)

            if cursor == 0:
                break
