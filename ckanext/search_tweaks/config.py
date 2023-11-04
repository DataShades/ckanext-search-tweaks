from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckan.lib.search.query import QUERY_FIELDS

CONFIG_QF = "ckanext.search_tweaks.common.qf"
DEFAULT_QF = QUERY_FIELDS

CONFIG_FUZZY = "ckanext.search_tweaks.common.fuzzy_search.enabled"
CONFIG_FUZZY_DISTANCE = "ckanext.search_tweaks.common.fuzzy_search.distance"
CONFIG_MM = "ckanext.search_tweaks.common.mm"
CONFIG_FUZZY_KEEP_ORIGINAL = "ckanext.search_tweaks.common.fuzzy_search.keep_original"
CONFIG_PREFER_BOOST = "ckanext.search_tweaks.common.prefer_boost"


def qf() -> str:
    return tk.config[CONFIG_QF] or DEFAULT_QF


def fuzzy() -> bool:
    return tk.config[CONFIG_FUZZY]


def fuzzy_distance() -> int:
    return tk.config[CONFIG_FUZZY_DISTANCE]


def mm() -> str:
    return tk.config[CONFIG_MM]


def fuzzy_with_original() -> bool:
    return tk.config[CONFIG_FUZZY_KEEP_ORIGINAL]


def prefer_boost() -> bool:
    return tk.config[CONFIG_PREFER_BOOST]
