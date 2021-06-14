from __future__ import annotations

from string import Template
from typing import Any, Optional

import ckan.plugins as p
import ckan.plugins.toolkit as tk

from ..interfaces import ISearchBoost

CONFIG_BOOST_FN = "ckanext.search_tweaks.field_relevance.boost_function"

DEFAULT_BOOST_FN = None

class FieldRelevancePlugin(p.SingletonPlugin):
    p.implements(ISearchBoost)

    def get_search_boost_fn(self, search_params: dict[str, Any]) -> Optional[str]:
        return tk.config.get(CONFIG_BOOST_FN, DEFAULT_BOOST_FN)
