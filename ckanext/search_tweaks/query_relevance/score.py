from .storage import (
    PermanentRedisScoreStorage,
    DailyRedisScoreStorage,
    ScoreStorage,
)
from .config import get_store_backend

_store_backends = {
    "redis-permanent": PermanentRedisScoreStorage,
    "redis-daily": DailyRedisScoreStorage,
}


def normalize_query(query: str) -> str:
    clean = "".join(
        char if char.isalnum() or char.isspace() else " "
        for char in query.strip().lower()
    )
    return " ".join(clean.split())


class QueryScore:
    storage_class: type[ScoreStorage]

    def __init__(
        self,
        id_: str,
        query: str,
        *,
        normalize: bool = True,
        storage_class: type[ScoreStorage] | None = None,
    ):
        if normalize:
            query = normalize_query(query)

        if storage_class:
            self.storage_class = storage_class
        else:
            self.storage_class = self.default_storage_class()
        self.storage = self.storage_class(id_, query)

    def __int__(self):
        return self.storage.get()

    @staticmethod
    def default_storage_class() -> type[ScoreStorage]:
        return _store_backends[get_store_backend()]

    @property
    def query(self):
        return self.storage.query

    def increase(self, n: int) -> None:
        self.storage.inc(n)

    def align(self):
        self.storage.align()

    def reset(self):
        self.storage.reset()

    @classmethod
    def get_all(cls):
        storage = cls.default_storage_class()
        return storage.scan()

    @classmethod
    def get_for_query(cls, query: str):
        storage = cls.default_storage_class()
        return storage.scan(query)
