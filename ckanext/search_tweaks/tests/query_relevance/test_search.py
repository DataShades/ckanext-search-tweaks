import pytest

from ckan.tests.helpers import call_action

from ckanext.search_tweaks.query_relevance import QueryScore


@pytest.mark.usefixtures("with_plugins", "clean_db", "clean_redis", "clean_index")
class TestSearchScoreBoost:
    def test_no_score_boost(self, dataset_factory):
        dataset_factory(title="ocean water")
        dataset_factory(title="water basin")

        result = call_action("package_search", q="water", fl="id,title,score")[
            "results"
        ]

        assert abs(result[0]["score"] - result[1]["score"]) < 0.01

    def test_query_relevance_disabled(self, dataset_factory):
        dataset_1 = dataset_factory(title="ocean water")
        dataset_2 = dataset_factory(title="water basin")

        QueryScore(dataset_1["id"], "water").increase(10)
        QueryScore(dataset_2["id"], "water").increase(5)

        result = call_action(
            "package_search",
            q="water",
            fl="id,title,score",
            extras={"ext_search_tweaks_disable_query_boost": True},
        )["results"]

        assert abs(result[0]["score"] - result[1]["score"]) < 0.01

    @pytest.mark.ckan_config("ckanext.search_tweaks.common.prefer_boost", "false")
    def test_query_relevance_boosted_with_bf(self, dataset_factory):
        dataset_1 = dataset_factory(title="ocean water")
        dataset_2 = dataset_factory(title="water basin")

        QueryScore(dataset_1["id"], "water").increase(10)
        QueryScore(dataset_2["id"], "water").increase(5)

        result = call_action("package_search", q="water", fl="id,title,score")[
            "results"
        ]

        assert abs(result[0]["score"] - result[1]["score"]) > 0.01

    @pytest.mark.ckan_config("ckanext.search_tweaks.common.prefer_boost", "true")
    def test_query_relevance_boosted_with_boost(self, dataset_factory):
        dataset_1 = dataset_factory(title="ocean water")
        dataset_2 = dataset_factory(title="water basin")

        QueryScore(dataset_1["id"], "water").increase(10)
        QueryScore(dataset_2["id"], "water").increase(5)

        result = call_action("package_search", q="water", fl="id,title,score")[
            "results"
        ]

        assert abs(result[0]["score"] - result[1]["score"]) > 0.01

    @pytest.mark.skip(reason="use only for profiling")
    def test_profile_boost_function(self, dataset_factory):
        first_query = None

        for _ in range(1000):
            dataset = dataset_factory()
            ds_query = dataset["title"].split()[0]

            if first_query is None:
                first_query = ds_query

            QueryScore(dataset["id"], ds_query).increase(1)

        import timeit

        def time_query():
            call_action("package_search", q=first_query, fl="id,title,score")

        time = timeit.timeit(time_query, number=20)

        print(f"Time: {time}")
