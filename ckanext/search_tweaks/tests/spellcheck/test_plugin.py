from unittest import mock

import pytest
from bs4 import BeautifulSoup

import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ckan.tests.factories import Dataset
from ckanext.search_tweaks.spellcheck import (
    CONFIG_SHOW_ONLY_MORE,
    rebuild_dictionary,
)


@pytest.mark.ckan_config("ckan.plugins", "search_tweaks search_tweaks_spellcheck")
@pytest.mark.usefixtures("with_plugins")
class TestSpellcheck:
    def test_plugin_loaded(self):
        assert p.plugin_loaded("search_tweaks_spellcheck")


@pytest.mark.ckan_config("ckan.plugins", "search_tweaks search_tweaks_spellcheck")
@pytest.mark.usefixtures("with_plugins", "with_request_context")
class TestDidYouMeanSnippet:
    def test_empty_without_data(self):
        assert not tk.render("search_tweaks/did_you_mean.html").strip()

    def test_with_query(self, monkeypatch):
        expected = "hello"
        helper = mock.Mock(return_value=[expected])
        monkeypatch.setitem(tk.h, "spellcheck_did_you_mean", helper)
        snippet = BeautifulSoup(tk.render("search_tweaks/did_you_mean.html"))
        helper.assert_called()
        link = snippet.select_one("a")
        assert link.text.strip() == expected
        assert "q=" + expected in link["href"]


@pytest.mark.ckanext_search_tweaks_modified_schema
@pytest.mark.ckan_config("ckan.plugins", "search_tweaks search_tweaks_spellcheck")
@pytest.mark.usefixtures("with_plugins", "clean_db", "clean_index")
class TestHelper:
    def test_recommendations(self):
        Dataset(title="Pick this")
        Dataset(notes="Pick this")
        Dataset(title="Do not touch me")
        helper = tk.h.spellcheck_did_you_mean
        rebuild_dictionary()
        assert helper("pick thes") == ["pick test"]
        assert helper("do nat touc me") == ["do not touch me"]

        assert helper("pic", 3) == [
            "pick"
        ]  # min_hits fucked up because of single-term match
        assert helper("pic", 1) == ["pick"]

    def test_show_only_more_results(self, ckan_config, monkeypatch):
        Dataset(title="Pick this")
        Dataset(notes="Pick this")
        Dataset(title="Pock this")
        rebuild_dictionary()
        helper = tk.h.spellcheck_did_you_mean

        assert helper("pock", 1) == ["pick"]
        assert helper("pick", 3) == [
            "pock"
        ]  # min_hits fucked up because of single-term match

        monkeypatch.setitem(ckan_config, CONFIG_SHOW_ONLY_MORE, "off")
        assert helper("pock", 1) == ["pick"]
        assert helper("pick", 2) == ["pock"]
