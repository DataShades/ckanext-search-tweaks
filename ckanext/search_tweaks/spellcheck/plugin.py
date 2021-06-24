from functools import reduce
from operator import itemgetter
from typing import Optional

from ckan.lib.search.common import make_connection

import ckan.plugins as p
import ckan.plugins.toolkit as tk
from .. import cli

CONFIG_EXTRA_PREFIX = "ckanext.search_tweaks.spellcheck.extra."
CONFIG_SHOW_ONLY_MORE = "ckanext.search_tweaks.spellcheck.more_results_only"

DEFAULT_SHOW_ONLY_MORE = True


def better_collation(left, right):
    return max(left, right, key=itemgetter("hits"))


def _get_spellcheck_params():
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
    for k in tk.config:
        if k.startswith(CONFIG_EXTRA_PREFIX):
            default[k[len(CONFIG_EXTRA_PREFIX) :]] = tk.config[k]
    return default


def rebuild_dictionary():
    spellcheck_params = _get_spellcheck_params()
    spellcheck_params["spellcheck.build"] = "true"
    spellcheck_params["spellcheck.reload"] = "true"
    conn = make_connection(decode_dates=False)
    conn.search(q="", rows=0, **spellcheck_params)


def spellcheck_did_you_mean(q: str, min_hits: int = 0) -> Optional[str]:
    if not q:
        return
    only_better_options = tk.asbool(tk.config.get(CONFIG_SHOW_ONLY_MORE, DEFAULT_SHOW_ONLY_MORE))
    spellcheck_params = _get_spellcheck_params()
    conn = make_connection(decode_dates=False)
    resp = conn.search(q=q, rows=0, **spellcheck_params)
    collations = resp.spellcheck.get("collations")
    if not collations and not only_better_options:
        suggestions = resp.spellcheck.get("suggestions", [])
        alternatives = dict(zip(suggestions[::2], [s["suggestion"][0] for s in suggestions[1::2]]))
        new_q = ' '.join([alternatives[w] for w in q.split() if w in alternatives])
        return new_q or None

    best = reduce(better_collation, collations[1::2])
    if not only_better_options:
        min_hits = -1
    if best["hits"] > min_hits:
        return best["collationQuery"]


class SpellcheckPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurable)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    # IConfigurable

    def configure(self, config):
        cli.search_tweaks.add_command(cli.spellcheck)

    # IConfigurer

    def update_config(self, config):
        tk.add_template_directory(config, "templates")

    # ITemplateHelpers

    def get_helpers(self):
        return {
            "spellcheck_did_you_mean": spellcheck_did_you_mean,
        }
