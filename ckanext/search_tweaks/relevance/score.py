from typing import Optional, Type
import ckan.plugins.toolkit as tk
from .storage import PermanentRedisScoreStorage, DailyRedisScoreStorage, ScoreStorage

_backends = {
    "redis-permanent": PermanentRedisScoreStorage,
    "redis-daily": DailyRedisScoreStorage,
}

CONFIG_BACKEND = "ckanext.search_tweaks.relevance.backend"
DEFAULT_BACKEND = "redis-daily"

DEFAULT_SCORE_STORAGE_CLASS = DailyRedisScoreStorage

_space_translation = str.maketrans({char: " " for char in """'",-!?.:"""})


def normalize_query(query: str) -> str:
    return " ".join(query.strip().lower().translate(_space_translation).split())


class QueryScore:
    storage_class: Type[ScoreStorage]

    def __init__(
        self,
        id_: str,
        query: str,
        *,
        normalize: bool = True,
        storage_class: Optional[Type[ScoreStorage]] = None
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
    def default_storage_class() -> Type[ScoreStorage]:
        return _backends[
            tk.config.get(CONFIG_BACKEND, DEFAULT_BACKEND)
        ]

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
    def get_for(cls, id_: str):
        return cls.default_storage_class().scan(id_)
