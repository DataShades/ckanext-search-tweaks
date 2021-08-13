from __future__ import annotations

from typing import Any, Optional

import ckan.plugins as p
import ckan.plugins.toolkit as tk

from . import views
from ..interfaces import ISearchTweaks
from .. import feature_disabled

CONFIG_BOOST_FN = "ckanext.search_tweaks.field_relevance.boost_function"

DEFAULT_BOOST_FN = None


class FieldRelevancePlugin(p.SingletonPlugin):
    p.implements(ISearchTweaks, inherit=True)
    p.implements(p.IBlueprint)
    p.implements(p.IConfigurer, inherit=True)

    # ISearchTweaks
    def get_search_boost_fn(self, search_params: dict[str, Any]) -> Optional[str]:
        if feature_disabled("field_boost", search_params):
            return

        return tk.config.get(CONFIG_BOOST_FN, DEFAULT_BOOST_FN)


    # IBlueprint

    def get_blueprint(self):
        return views.get_blueprints()

    # IConfigurer

    def update_config(self, config):
        tk.add_template_directory(config, "templates")
        tk.add_resource("assets", "search_tweaks_field_relevance")
