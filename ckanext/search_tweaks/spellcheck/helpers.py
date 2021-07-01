from __future__ import annotations


from functools import reduce
from operator import itemgetter
from typing import Optional
from typing_extensions import TypedDict

import ckan.plugins.toolkit as tk
from ckan.lib.search.common import make_connection

from . import get_spellcheck_params, CONFIG_SHOW_ONLY_MORE, DEFAULT_SHOW_ONLY_MORE


def get_helpers():
    return {
        "spellcheck_did_you_mean": spellcheck_did_you_mean,
    }


class Collation(TypedDict):
    hits: int
    collationQuery: str


def _better_collation(left: Collation, right: Collation) -> Collation:
    return max(left, right, key=itemgetter("hits"))


def spellcheck_did_you_mean(q: str, min_hits: int = 0) -> Optional[str]:
    """Return optimal query that can be used instead of the current one.

    Suggested query is guaranteed to have at least `min_hits` matching
    documents. Note though that it avoids all the CKAN plugins, so after
    suggested query applied to the `package_search` action, number of results
    may be different.

    """
    if not q:
        return

    spellcheck_params = get_spellcheck_params()
    conn = make_connection(decode_dates=False)
    resp = conn.search(q=q, rows=0, **spellcheck_params)
    collations = resp.spellcheck.get("collations")

    show_only_more = tk.asbool(
        tk.config.get(CONFIG_SHOW_ONLY_MORE, DEFAULT_SHOW_ONLY_MORE)
    )

    # TODO: make this section optional depending on the params
    if not collations and not show_only_more:
        # this is a bit tricky part. We are collecting brand new query from the
        # best suggestions for each separate token in the original
        # query. Result of this operation is likely to be the nonesense from
        # the human's point of view, but Solr will gladely accept it.
        suggestions = resp.spellcheck.get("suggestions", [])
        alternatives: dict[str, str] = dict(
            zip(suggestions[::2], [s["suggestion"][0] for s in suggestions[1::2]])
        )
        new_q = " ".join([alternatives[w] for w in q.split() if w in alternatives])
        return new_q or None

    best = reduce(_better_collation, collations[1::2])
    if not show_only_more:
        min_hits = -1

    if best["hits"] > min_hits:
        return best["collationQuery"]
