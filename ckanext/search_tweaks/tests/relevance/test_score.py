import pytest
from ckanext.search_tweaks.relevance import QueryScore


class TestQueryScore:
    def test_disabled_normalization(self):
        query = "Hey, YOU!"
        score = QueryScore("random", query, normalize=False)
        assert score.query == query

    @pytest.mark.parametrize(
        "query, normalized",
        [
            ("Hello World", "hello world"),
            (" h-e, l    l! o.w orLD ", "h e l l o w orld"),
        ],
    )
    def test_normalize(self, query, normalized):
        score = QueryScore("random", query)
        assert score.query == normalized

    def test_stored_queries(self):
        QueryScore("first", "hello").reset()
        QueryScore("second", "world").reset()

        QueryScore("first", "hello").increase(1)
        QueryScore("second", "world").increase(1)
        assert int(QueryScore("first", "hello")) == 1
        assert int(QueryScore("second", "world")) == 1

        QueryScore("first", "hello").increase(5)
        QueryScore("second", "world").increase(10)
        assert int(QueryScore("first", "hello")) == 6
        assert int(QueryScore("second", "world")) == 11
