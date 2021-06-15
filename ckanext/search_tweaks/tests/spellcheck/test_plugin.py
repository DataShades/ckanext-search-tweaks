from unittest import mock

import pytest
from bs4 import BeautifulSoup

import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ckan.tests.factories import Dataset


@pytest.mark.ckan_config("ckan.plugins", "search_tweaks search_tweaks_spellcheck")
@pytest.mark.usefixtures("with_plugins")
class TestSpellcheck:
    def test_plugin_loaded(self):
        assert p.plugin_loaded("search_tweaks_spellcheck")

@pytest.mark.ckan_config("ckan.plugins", "search_tweaks search_tweaks_spellcheck")
@pytest.mark.usefixtures("with_plugins", "with_request_context")
class TestDidYouMeanSnippet:
    def test_empty_without_data(self):
        assert not tk.render("search_tweaks/did_you_mean.html")

    def test_with_query(self, monkeypatch):
        expected = "hello"
        helper = mock.Mock(return_value=expected)
        monkeypatch.setitem(tk.h, 'spellcheck_did_you_mean', helper)
        snippet = BeautifulSoup(tk.render("search_tweaks/did_you_mean.html"))
        helper.assert_called()
        link = snippet.select_one("a")
        assert link.text.strip() == expected
        assert "q=" + expected in link["href"]



@pytest.mark.ckan_config("ckan.plugins", "search_tweaks search_tweaks_spellcheck")
@pytest.mark.usefixtures("with_plugins", "clean_db", "clean_index")
class TestHelper:
    def test_recommendations(self):
        Dataset(title="Pick this")
        Dataset(notes="Pick this")
        Dataset(title="Do not touch me")
        helper = tk.h.spellcheck_did_you_mean

        assert helper("pic thes") == "pick this"
        assert helper("do nat touc me") == "do not touch me"

        assert helper("pic", 2) is None
        assert helper("pic", 1) == "pick"
