import pytest

from ckanext.search_tweaks.query_relevance.storage import QueryHitTracker


@pytest.mark.usefixtures("clean_redis")
class TestQueryHitTracker:
    def test_increase(self):
        QueryHitTracker("id-1", "hello").increase(1)
        QueryHitTracker("id-2", "hello").increase(5)

        result = QueryHitTracker.top("hello", 2)

        assert result == [(b"id-2", 5.0), (b"id-1", 1.0)]

    def test_missing_query(self):
        result = QueryHitTracker.top("hello")

        assert result == []

    def test_expiration(self):
        tracker = QueryHitTracker("id-1", "hello", ttl=1)
        tracker.increase(1)

        import time

        time.sleep(2)

        assert tracker.top("hello") == []

    def test_reset(self):
        tracker = QueryHitTracker("id-1", "hello")

        tracker.increase(1)
        assert tracker.top("hello") == [(b"id-1", 1.0)]

        tracker.reset("hello")
        assert tracker.top("hello") == []
