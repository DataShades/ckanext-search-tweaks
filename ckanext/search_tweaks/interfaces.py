from __future__ import annotations
from typing import Any, Optional

from ckan.plugins.interfaces import Interface


class ISearchBoost(Interface):

    def get_search_boost_fn(self, search_params: dict[str, Any]) -> Optional[str]:
        """Return Solr's bf applicable to the current search.
        """
        return None
