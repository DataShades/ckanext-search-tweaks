from __future__ import annotations

from typing import Any, Optional

import ckan.plugins as p
import ckan.plugins.toolkit as tk

from ..interfaces import ISearchTweaks
from .. import feature_disabled

CONFIG_BOOST_FN = "ckanext.search_tweaks.field_relevance.boost_function"

DEFAULT_BOOST_FN = None


class FieldRelevancePlugin(p.SingletonPlugin):
    p.implements(ISearchTweaks, inherit=True)

    def get_search_boost_fn(self, search_params: dict[str, Any]) -> Optional[str]:
        if feature_disabled("field_boost", search_params):
            return

        return tk.config.get(CONFIG_BOOST_FN, DEFAULT_BOOST_FN)
