from __future__ import annotations

from functools import total_ordering
from typing import Any, Optional

import ckan.plugins.toolkit as tk
from ckan.lib.search.common import make_connection

from . import get_spellcheck_params, CONFIG_SHOW_ONLY_MORE, DEFAULT_SHOW_ONLY_MORE

CONFIG_MAX_SUGGESTIONS = "ckanext.search_tweaks.spellcheck.max_suggestions"
CONFIG_SUGGESTION_FOR_SINGLE = (
    "ckanext.search_tweaks.spellcheck.single_term_prefer_suggestion"
)

DEFAULT_MAX_SUGGESTIONS = 1
DEFAULT_SUGGESTION_FOR_SINGLE = True


def get_helpers():
    return {
        "spellcheck_did_you_mean": spellcheck_did_you_mean,
    }


def spellcheck_did_you_mean(
    q: str, min_hits: int = 0, max_suggestions: int = None
) -> list[str]:
    """Return optimal query that can be used instead of the current one.

    Suggested query is guaranteed to have at least `min_hits` matching
    documents. Note though that it avoids all the CKAN plugins, so after
    suggested query applied to the `package_search` action, number of results
    may be different.

    """
    if not q:
        return []

    spellcheck = _do_spellcheck(q)

    show_only_more = tk.asbool(
        tk.config.get(CONFIG_SHOW_ONLY_MORE, DEFAULT_SHOW_ONLY_MORE)
    )
    if not show_only_more:
        min_hits = -1

    if not max_suggestions:
        max_suggestions = tk.asint(
            tk.config.get(CONFIG_MAX_SUGGESTIONS, DEFAULT_MAX_SUGGESTIONS)
        )

    use_suggestion_for_single = tk.asbool(
        tk.config.get(CONFIG_SUGGESTION_FOR_SINGLE, DEFAULT_SUGGESTION_FOR_SINGLE)
    )
    terms = q.split()
    if len(terms) == 1 and use_suggestion_for_single:
        # TODO: check min hits
        return spellcheck.suggestions.get(terms[0], [])[:max_suggestions]

    collations = [
        str(c) for c in spellcheck.best_collations(max_suggestions) if min_hits < c
    ]

    if len(collations) < max_suggestions:
        # this is a bit tricky part. We are collecting brand new query from the
        # best suggestions for each separate token in the original
        # query. Result of this operation is likely to be the nonesense from
        # the human's point of view, but Solr will gladely accept it.

        # TODO: check min hits
        new_q = " ".join(
            [spellcheck.suggestions[w][0] for w in terms if w in spellcheck.suggestions]
        )
        collations.append(new_q)

    return collations


def _do_spellcheck(q):
    spellcheck_params = get_spellcheck_params()
    conn = make_connection(decode_dates=False)
    result = conn.search(q=q, rows=0, **spellcheck_params).spellcheck
    return SpellcheckResult(
        result.get("collations", []),
        result.get("suggestions", []),
    )


@total_ordering
class Collation:
    hits: int
    query: str
    corrections: dict[str, str]

    def __repr__(self):
        return f"<Collation({self.hits}): {self.query}>"

    def __init__(self, data: dict[str, Any]):
        self.hits = data["hits"]
        self.query = data["collationQuery"]
        changes = data["misspellingsAndCorrections"]
        self.corrections = dict(zip(changes[::2], changes[1::2]))

    def __eq__(self, other):
        if isinstance(other, int):
            return self.hits == other
        return self.hits == other.hits and self.query == other.query

    def __gt__(self, other):
        if isinstance(other, int):
            return self.hits > other

        if self.hits == other.hits:
            return self.query > other.query

        return self.hits > other.hits

    def __str__(self):
        return self.query

    def __int__(self):
        return self.hits


class SpellcheckResult:
    collations: list[Collation]
    suggestions: dict[str, list[str]]

    def __repr__(self):
        return f"<Spellcheck(collations={self.collations}, suggestions={self.suggestions})>"

    def __init__(self, collations: list[Any], suggestions: list[Any]):
        self.collations = [Collation(item) for item in collations[1::2]]
        self.suggestions = dict(
            zip(suggestions[::2], [s["suggestion"] for s in suggestions[1::2]])
        )

    def best_collations(self, n: Optional[int] = None) -> list[Collation]:
        return sorted(self.collations)[:n]
