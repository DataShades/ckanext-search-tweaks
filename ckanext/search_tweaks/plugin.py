from __future__ import annotations

import logging

from typing import Any, Dict
import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
from ckan.lib.search.query import QUERY_FIELDS

from . import cli
from .interfaces import ISearchTweaks

log = logging.getLogger(__name__)

SearchParams = Dict[str, Any]

CONFIG_QF = "ckanext.search_tweaks.common.qf"
CONFIG_FUZZY = "ckanext.search_tweaks.common.fuzzy_search.enabled"
CONFIG_FUZZY_DISTANCE = "ckanext.search_tweaks.common.fuzzy_search.distance"
CONFIG_PREFER_BOOST = "ckanext.search_tweaks.common.prefer_boost"
CONFIG_MM = "ckanext.search_tweaks.common.mm"

DEFAULT_QF = QUERY_FIELDS
DEFAULT_FUZZY = False
DEFAULT_FUZZY_DISTANCE = 1
DEFAULT_PREFER_BOOST = False
DEFAULT_MM = "1"

class SearchTweaksPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IClick

    def get_commands(self):
        return cli.get_commands()

    # IPackageController

    def before_search(self, search_params: SearchParams):
        search_params.setdefault("mm", tk.config.get(CONFIG_MM, DEFAULT_MM))
        if "defType" not in search_params:
            search_params["defType"] = "edismax"
        prefer_boost = tk.asbool(tk.config.get(CONFIG_PREFER_BOOST, DEFAULT_PREFER_BOOST))

        if prefer_boost and search_params["defType"] == "edismax":
            _set_boost(search_params)
        else:
            _set_bf(search_params)
        _set_qf(search_params)
        _set_fuzzy(search_params)

        return search_params


def _set_boost(search_params: SearchParams):
    boost = search_params.setdefault("boost", [])
    for plugin in plugins.PluginImplementations(ISearchTweaks):
        extra = plugin.get_search_boost_fn(search_params)
        if not extra:
            continue
        boost.append(extra)


def _set_bf(search_params: SearchParams):
    default_bf = search_params.get("bf") or "0"
    search_params.setdefault("bf", default_bf)
    for plugin in plugins.PluginImplementations(ISearchTweaks):
        extra_bf = plugin.get_search_boost_fn(search_params)
        if not extra_bf:
            continue
        search_params["bf"] = f"sum({search_params['bf']},{extra_bf})"


def _set_qf(search_params: SearchParams):
    default_qf = search_params.get("qf") or tk.config.get(CONFIG_QF, DEFAULT_QF)
    search_params.setdefault("qf", default_qf)
    for plugin in plugins.PluginImplementations(ISearchTweaks):
        extra_qf = plugin.get_extra_qf(search_params)
        if not extra_qf:
            continue
        search_params["qf"] += " " + extra_qf


def _set_fuzzy(search_params: SearchParams):
    if not tk.asbool(tk.config.get(CONFIG_FUZZY, DEFAULT_FUZZY)):
        return
    distance = tk.asint(tk.config.get(CONFIG_FUZZY_DISTANCE, DEFAULT_FUZZY_DISTANCE))
    if distance < 0:
        log.warning("Cannot use negative fuzzy distance: %s.", distance)
        distance = 0
    elif distance > 2:
        log.warning(
            "Cannot use fuzzy distance greater than 2: %s. Reduce it to top boundary",
            distance,
        )
        distance = 2

    if not distance:
        return

    q = search_params.get("q")
    if not q:
        return
    if not set(""":"'~""") & set(q):
        search_params["q"] = " ".join(
            map(
                lambda s: f"{s}~{distance}"
                if s.isalpha() and s not in ("AND", "OR", "TO")
                else s,
                q.split(),
            )
        )
