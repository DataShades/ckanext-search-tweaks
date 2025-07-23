from .storage import QueryHitTracker
from .config import get_max_boost_count


def normalize_query(query: str) -> str:
    clean = "".join(
        char if char.isalnum() or char.isspace() else " "
        for char in query.strip().lower()
    )
    return " ".join(clean.split())


class QueryScore:
    def __init__(self, entity_id: str, query: str, normalize: bool = True):
        if normalize:
            query = normalize_query(query)

        self.entity_id = entity_id
        self.query = query

        self.storage = QueryHitTracker(self.entity_id, self.query)

    def __int__(self):
        return self.storage.get()

    def increase(self, amount: int) -> None:
        self.storage.increase(amount)

    def reset(self):
        self.storage.reset(self.query)

    @classmethod
    def get_for_query(cls, query: str, limit: int | None = None) -> list[tuple[bytes, float]]:
        return QueryHitTracker.top(query, limit or get_max_boost_count())

    @classmethod
    def get_all(cls):
        return QueryHitTracker.get_all()

    @classmethod
    def reset_all(cls):
        return QueryHitTracker.reset_all()
