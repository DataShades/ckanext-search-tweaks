import pytest

import ckan.plugins as p
import ckan.lib.search.query as query

from ckanext.search_tweaks import CONFIG_PREFER_BOOST
import ckanext.search_tweaks.plugin as plugin


@pytest.mark.usefixtures("with_plugins")
def test_plugin_loaded():
    assert p.plugin_loaded("search_tweaks")


@pytest.mark.usefixtures("with_plugins")
class TestPlugin:
    def test_deftype(self, search):
        assert search()["defType"] == "edismax"
        assert search(defType="dismax")["defType"] == "dismax"

    @pytest.mark.ckan_config(CONFIG_PREFER_BOOST, "no")
    def test_default_bf(self, search):
        assert search()["bf"] == "0"

    @pytest.mark.ckan_config(CONFIG_PREFER_BOOST, "no")
    def test_modified_bf(self, search):
        result = search(bf="sum(0,1)")
        assert result["bf"] == "sum(0,1)"
        assert "boost" not in result

    @pytest.mark.ckan_config(CONFIG_PREFER_BOOST, "no")
    def test_boost_is_disabled(self, search):
        assert "boost" not in search()

    def test_boost_enabled_by_default_and_empty(self, search):
        result = search()
        assert "bf" not in result
        assert result["boost"] == []

    def test_boost_modified(self, search):
        result = search(boost=["0", "1"])
        assert "bf" not in result
        assert result["boost"] == ["0", "1"]

    def test_default_qf(self, search):
        assert search()["qf"] == query.QUERY_FIELDS

    @pytest.mark.ckan_config(plugin.CONFIG_QF, "title^10 name^0.1")
    def test_modified_qf(self, search):
        assert search()["qf"] == "title^10 name^0.1"


@pytest.mark.usefixtures("with_plugins")
class TestFuzzy:
    def test_fuzzy_disabled(self, search):
        assert search()["q"] == "*:*"
        assert search(q="hello")["q"] == "hello"
        assert search(q="hello world")["q"] == "hello world"
        assert search(q="hello:world")["q"] == "hello:world"
        assert search(q="hello AND world")["q"] == "hello AND world"

    @pytest.mark.ckan_config(plugin.CONFIG_FUZZY, "on")
    @pytest.mark.parametrize("distance", [1, 2])
    def test_fuzzy_enabled(self, search, distance, ckan_config, monkeypatch):
        monkeypatch.setitem(ckan_config, plugin.CONFIG_FUZZY_DISTANCE, distance)
        assert search()["q"] == "*:*"
        assert search(q="hello")["q"] == f"hello~{distance}"
        assert search(q="hello world")["q"] == f"hello~{distance} world~{distance}"
        assert search(q="hello:world")["q"] == f"hello:world"
        assert (
            search(q="hello AND world")["q"] == f"hello~{distance} AND world~{distance}"
        )

    @pytest.mark.ckan_config(plugin.CONFIG_FUZZY, "on")
    @pytest.mark.parametrize("distance", [-10, -1, 0])
    def test_fuzzy_enabled_with_too_low_distance(
        self, search, distance, ckan_config, monkeypatch
    ):
        monkeypatch.setitem(ckan_config, plugin.CONFIG_FUZZY_DISTANCE, distance)
        assert search(q="")["q"] == "*:*"
        assert search(q="hello")["q"] == "hello"
        assert search(q="hello world")["q"] == "hello world"
        assert search(q="hello:world")["q"] == "hello:world"
        assert search(q="hello AND world")["q"] == "hello AND world"

    @pytest.mark.ckan_config(plugin.CONFIG_FUZZY, "on")
    @pytest.mark.parametrize("distance", [3, 20, 111])
    def test_fuzzy_enabled_with_too_high_distance(
        self, search, distance, ckan_config, monkeypatch
    ):
        monkeypatch.setitem(ckan_config, plugin.CONFIG_FUZZY_DISTANCE, distance)
        assert search()["q"] == "*:*"
        assert search(q="hello")["q"] == "hello~2"
        assert search(q="hello world")["q"] == "hello~2 world~2"
        assert search(q="hello:world")["q"] == "hello:world"
        assert search(q="hello AND world")["q"] == "hello~2 AND world~2"
