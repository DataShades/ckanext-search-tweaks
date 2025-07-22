from __future__ import annotations

from typing import Any

import ckan.plugins as p
import ckan.plugins.toolkit as tk

from ckanext.search_tweaks.interfaces import ISearchTweaks
from ckanext.search_tweaks.shared import feature_disabled

CONFIG_BOOST_FN = "ckanext.search_tweaks.field_relevance.boost_function"

DEFAULT_BOOST_FN = None


@tk.blanket.blueprints
class FieldRelevancePlugin(p.SingletonPlugin):
    p.implements(ISearchTweaks, inherit=True)
    p.implements(p.IAuthFunctions)
    p.implements(p.IConfigurer, inherit=True)

    # ISearchTweaks
    def get_search_boost_fn(self, search_params: dict[str, Any]) -> str | None:
        if feature_disabled("field_boost", search_params):
            return None

        return tk.config.get(CONFIG_BOOST_FN, DEFAULT_BOOST_FN)

    # IConfigurer

    def update_config(self, config):
        tk.add_template_directory(config, "templates")
        tk.add_resource("assets", "search_tweaks_field_relevance")

    # IAuthFunctions
    def get_auth_functions(self):
        return {
            "search_tweaks_field_relevance_promote": promote_auth,
        }


def promote_auth(context, data_dict):
    try:
        tk.check_access("package_update", context, data_dict)
    except tk.NotAuthorized:
        return {"success": False}

    return {"success": True}
