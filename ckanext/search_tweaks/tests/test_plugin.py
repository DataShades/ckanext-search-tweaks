import types
from unittest import mock
from typing import cast

import pytest

import ckan.plugins as p
import ckan.lib.search.query as query
from ckan.tests.helpers import call_action

import ckanext.search_tweaks.plugin as plugin


@pytest.fixture
def search(monkeypatch):
    """Call package_search and return dict, passed to search_query.run"""
    run = query.PackageSearchQuery.run
    patch = cast(
        mock.Mock,
        types.MethodType(mock.Mock(side_effect=run), query.PackageSearchQuery),
    )

    monkeypatch.setattr(query.PackageSearchQuery, "run", patch)

    def expose_args(*args, **kwargs):
        call_action("package_search", *args, **kwargs)
        return patch.call_args.args[1]

    return expose_args


def test_plugin_loaded():
    assert p.plugin_loaded("search_tweaks")


class TestPlugin:
    def test_deftype(self, search):
        assert search()["defType"] == "edismax"
        assert search(defType="dismax")["defType"] == "dismax"

    def test_bf(self, search):
        assert search()["bf"] == "0"

    def test_qf(self, search):
        assert search()["qf"] == query.QUERY_FIELDS

    @pytest.mark.ckan_config(plugin.CONFIG_QF, "title^10 name^0.1")
    def test_qf_configured(self, search):
        assert search()["qf"] == "title^10 name^0.1"


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
