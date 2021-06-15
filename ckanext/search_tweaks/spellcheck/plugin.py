from functools import reduce
from operator import itemgetter
from typing import Optional

from ckan.lib.search.common import make_connection

import ckan.plugins as p
import ckan.plugins.toolkit as tk

CONFIG_EXTRA_PREFIX = "ckanext.search_tweaks.spellcheck.extra."

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
            default[k[len(CONFIG_EXTRA_PREFIX):]] = tk.config[k]
    return default


def spellcheck_did_you_mean(q: str, min_hits: int = 0) -> Optional[str]:
    if not q:
        return
    spellcheck_params = _get_spellcheck_params()
    conn = make_connection(decode_dates=False)
    resp = conn.search(q=q, rows=0, **spellcheck_params)
    collations = resp.spellcheck.get('collations')
    if collations:
        best = reduce(better_collation, collations[1::2])
        if best["hits"] > min_hits:
            return best['collationQuery']


class SpellcheckPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config):
        tk.add_template_directory(config, "templates")

    # ITemplateHelpers

    def get_helpers(self):
        return {
            "spellcheck_did_you_mean": spellcheck_did_you_mean,
        }
