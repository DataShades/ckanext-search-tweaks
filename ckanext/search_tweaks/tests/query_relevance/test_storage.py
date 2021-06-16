import pytest
from ckanext.search_tweaks.query_relevance.storage import (
    DailyRedisScoreStorage,
    PermanentRedisScoreStorage,
)


@pytest.fixture
def storage(storage_class):
    storage_class.reset_storage()
    return storage_class


@pytest.mark.parametrize(
    "storage_class",
    [
        PermanentRedisScoreStorage,
        DailyRedisScoreStorage,
    ],
)
class TestStorages:
    def test_scan(self, storage):
        assert list(storage.scan()) == []

        s1 = storage("key", "query")
        s1.inc(10)
        assert sorted(list(storage.scan())) == sorted(
            [
                ("key", "query", 10),
            ]
        )

        s2 = storage("second key", "second query")
        s2.inc(5)
        s1.inc(90)
        assert sorted(list(storage.scan())) == sorted(
            [
                ("key", "query", 100),
                ("second key", "second query", 5),
            ]
        )

        s3 = storage("key", "extra query")
        s3.inc(1)
        assert sorted(list(storage.scan())) == sorted(
            [
                ("key", "query", 100),
                ("key", "extra query", 1),
                ("second key", "second query", 5),
            ]
        )

        assert sorted(list(storage.scan("key"))) == sorted(
            [
                ("key", "query", 100),
                ("key", "extra query", 1),
            ]
        )

    def test_missing_key(self, storage):
        s = storage("not a real key", "not a real query")
        assert s.get() == 0

    def test_set_and_reset(self, storage):
        s = storage("real key", "real value")
        s.set(10)
        assert s.get() == 10
        s.reset()
        assert s.get() == 0

    def test_increases(self, storage):
        s1 = storage("real key", "hello")
        s2 = storage("real key", "world")

        s1.inc(1)
        s2.inc(1)
        s1.inc(1)
        assert s1.get() == 2
        assert s2.get() == 1


class TestDailyStorage:
    @pytest.fixture(autouse=True)
    def reset_storage(self):
        DailyRedisScoreStorage.reset_storage()

    def test_score_aggregated(self, freezer):
        s = DailyRedisScoreStorage("key", "query")
        freezer.move_to("2012-01-01")
        s.inc(2)
        assert s.get() == 2

        freezer.move_to("2012-02-10")
        s.inc(1)
        assert s.get() == 3

        freezer.move_to("2012-03-26")
        s.inc(2)
        assert s.get() == 5

    def test_score_aligned(self, freezer):
        s = DailyRedisScoreStorage("key", "query")
        freezer.move_to("2010-01-01")
        s.inc(2)
        freezer.move_to("2011-01-01")
        s.inc(2)

        freezer.move_to("2012-02-10")
        s.inc(1)
        freezer.move_to("2012-03-26")
        s.inc(2)
        assert s.get() == 7
        s.align()
        assert s.get() == 3
