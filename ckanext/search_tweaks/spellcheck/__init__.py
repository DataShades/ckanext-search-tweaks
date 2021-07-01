from __future__ import annotations

from typing import Any

from ckan.lib.search.common import make_connection
import ckan.plugins.toolkit as tk


CONFIG_EXTRA_PREFIX = "ckanext.search_tweaks.spellcheck.extra."
CONFIG_SHOW_ONLY_MORE = "ckanext.search_tweaks.spellcheck.more_results_only"

DEFAULT_SHOW_ONLY_MORE = True


def get_spellcheck_params() -> dict[str, Any]:
    default = {
        "spellcheck": "on",
        "spellcheck.collate": "on",
        "spellcheck.collateExtendedResults": "on",
        "spellcheck.alternativeTermCount": 5,
        "spellcheck.count": 10,
        "spellcheck.maxResultsForSuggest": 5,
        "spellcheck.maxCollationTries": 10,
        "spellcheck.maxCollations": 5,
        "spellcheck.dictionary": "did_you_mean",
        "df": "did_you_mean",
    }
    unprefixed = slice(len(CONFIG_EXTRA_PREFIX), None)
    for k in tk.config:
        if k.startswith(CONFIG_EXTRA_PREFIX):
            default[k[unprefixed]] = tk.config[k]
    return default


def rebuild_dictionary():
    """Make sure our suggestions dictionary reflects current state of datasets.

    I'm fast enough, but don't call me too often.
    """
    spellcheck_params = get_spellcheck_params()
    spellcheck_params["spellcheck.build"] = "true"
    spellcheck_params["spellcheck.reload"] = "true"
    conn = make_connection(decode_dates=False)
    conn.search(q="", rows=0, **spellcheck_params)
