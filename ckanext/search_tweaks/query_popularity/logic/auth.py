from __future__ import annotations

from typing import Any

from ckan import types
from ckan.authz import is_authorized


def search_tweaks_query_popularity_list(
    context: types.Context,
    data_dict: dict[str, Any],
) -> types.AuthResult:
    return is_authorized("sysadmin", context, data_dict)


def search_tweaks_query_popularity_export(
    context: types.Context,
    data_dict: dict[str, Any],
) -> types.AuthResult:
    return is_authorized("sysadmin", context, data_dict)


def search_tweaks_query_popularity_ignore(
    context: types.Context,
    data_dict: dict[str, Any],
) -> types.AuthResult:
    return is_authorized("sysadmin", context, data_dict)
