from __future__ import annotations
from typing import Any
from ckan import types
import ckan.plugins.toolkit as tk

from ckanext.search_tweaks.query_popularity.score import Score


@tk.side_effect_free
def search_tweaks_query_popularity_list(
    context: types.Context, data_dict: dict[str, Any]
) -> list[dict[str, Any]]:
    score = Score()

    if tk.asbool(data_dict.get("refresh")):
        score.refresh()


    limit = tk.asint(data_dict.get("limit", 10))

    return list(score.stats(limit))
