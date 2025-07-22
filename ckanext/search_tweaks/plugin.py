from __future__ import annotations

import logging
from typing import Any

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk

from . import config
from .interfaces import ISearchTweaks
from .shared import feature_disabled

log = logging.getLogger(__name__)
CONFIG_PREFER_BOOST = "ckanext.search_tweaks.common.prefer_boost"
DEFAULT_PREFER_BOOST = True


@tk.blanket.cli
@tk.blanket.config_declarations
class SearchTweaksPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IPackageController, inherit=True)

    # IPackageController

    def before_dataset_search(self, search_params: dict[str, Any]):
        if feature_disabled("everything", search_params):
            return search_params

        search_params.setdefault("mm", config.mm())

        if "defType" not in search_params:
            search_params["defType"] = "edismax"

        if config.prefer_boost() and search_params["defType"] == "edismax":
            _set_boost(search_params)
        else:
            _set_bf(search_params)

        _set_qf(search_params)
        _set_fuzzy(search_params)

        return search_params


def _set_boost(search_params: dict[str, Any]) -> None:
    boost: list[str] = search_params.setdefault("boost", [])
    for plugin in plugins.PluginImplementations(ISearchTweaks):
        extra = plugin.get_search_boost_fn(search_params)
        if not extra:
            continue
        boost.append(extra)


def _set_bf(search_params: dict[str, Any]) -> None:
    default_bf: str = search_params.get("bf") or "0"
    search_params.setdefault("bf", default_bf)
    for plugin in plugins.PluginImplementations(ISearchTweaks):
        extra_bf = plugin.get_search_boost_fn(search_params)
        if not extra_bf:
            continue
        search_params["bf"] = f"sum({search_params['bf']},{extra_bf})"


def _set_qf(search_params: dict[str, Any]) -> None:
    if feature_disabled("qf", search_params):
        return

    default_qf: str = search_params.get("qf") or config.qf()
    search_params.setdefault("qf", default_qf)
    for plugin in plugins.PluginImplementations(ISearchTweaks):
        extra_qf = plugin.get_extra_qf(search_params)
        if not extra_qf:
            continue
        search_params["qf"] += " " + extra_qf


def _set_fuzzy(search_params: dict[str, Any]) -> None:
    if not config.fuzzy() or feature_disabled("fuzzy", search_params):
        return

    distance = _get_fuzzy_distance()
    if not distance:
        return

    q = search_params.get("q")
    if not q:
        return

    if set(""":"'~""") & set(q):
        return

    fuzzy_q = " ".join(
        map(
            lambda s: (
                f"{s}~{distance}" if s.isalpha() and s not in ("AND", "OR", "TO") else s
            ),
            q.split(),
        ),
    )
    if config.fuzzy_with_original():
        search_params["q"] = f"({fuzzy_q}) OR ({q})"
    else:
        search_params["q"] = fuzzy_q


def _get_fuzzy_distance() -> int:
    distance = config.fuzzy_distance()
    if distance < 0:
        log.warning("Cannot use negative fuzzy distance: %s.", distance)
        distance = 0
    elif distance > 2:
        log.warning(
            "Cannot use fuzzy distance greater than 2: %s. Reduce it to top boundary",
            distance,
        )
        distance = 2
    return distance
