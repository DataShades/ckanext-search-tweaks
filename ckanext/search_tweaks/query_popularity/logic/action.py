from __future__ import annotations

from typing import Any

import ckan.plugins.toolkit as tk
from ckan import types
from ckan.logic import validate

from ckanext.search_tweaks.query_popularity.score import Score

from . import schema


@tk.side_effect_free
def search_tweaks_query_popularity_list(
    context: types.Context,
    data_dict: dict[str, Any],
) -> list[dict[str, Any]]:
    score = Score()

    if tk.asbool(data_dict.get("refresh")):
        score.refresh()

    limit = tk.asint(data_dict.get("limit", 10))

    return list(score.stats(limit))


@tk.side_effect_free
def search_tweaks_query_popularity_export(
    context: types.Context,
    data_dict: dict[str, Any],
) -> list[Any]:
    score = Score()

    return score.export()


@validate(schema.query_popularity_import)
def search_tweaks_query_popularity_import(
    context: types.Context,
    data_dict: dict[str, Any],
) -> dict[str, Any]:
    tk.check_access("sysadmin", context, data_dict)
    score = Score()

    if tk.asbool(data_dict.get("reset")):
        score.reset()
    score.restore(data_dict["snapshot"])
    score.refresh()
    return {"success": True}


def search_tweaks_query_popularity_ignore(
    context: types.Context,
    data_dict: dict[str, Any],
):
    q = tk.get_or_bust(data_dict, "q")
    score = Score()
    result = score.ignore(q)
    if tk.asbool(data_dict.get("remove")):
        score.drop(q)

    return result
