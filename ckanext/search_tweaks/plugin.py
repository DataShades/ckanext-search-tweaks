from __future__ import annotations

from typing import Any
import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
from ckan.lib.search.query import QUERY_FIELDS

from . import cli
from .interfaces import ISearchTweaks

CONFIG_QF = "ckanext.search_tweaks.common.qf"
DEFAULT_QF = QUERY_FIELDS


class SearchTweaksPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IClick

    def get_commands(self):
        return cli.get_commands()

    # IPackageController

    def before_search(self, search_params: dict[str, Any]):
        if "defType" not in search_params:
            search_params["defType"] = "edismax"

        default_bf = search_params.get("bf") or "0"
        search_params.setdefault("bf", default_bf)
        for plugin in plugins.PluginImplementations(ISearchTweaks):
            extra_bf = plugin.get_search_boost_fn(search_params)
            if not extra_bf:
                continue
            search_params["bf"] = f"sum({search_params['bf']},{extra_bf})"

        default_qf = search_params.get("qf") or tk.config.get(CONFIG_QF, DEFAULT_QF)
        search_params.setdefault("qf", default_qf)
        for plugin in plugins.PluginImplementations(ISearchTweaks):
            extra_qf = plugin.get_extra_qf(search_params)
            if not extra_qf:
                continue
            search_params["qf"] += " " + extra_qf

        return search_params
