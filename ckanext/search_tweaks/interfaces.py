from __future__ import annotations
from typing import Any, Optional

from ckan.plugins.interfaces import Interface
from . import CONFIG_PREFER_BOOST


class ISearchTweaks(Interface):
    def get_search_boost_fn(self, search_params: dict[str, Any]) -> Optional[str]:
        f"""Return Solr's boost function applicable to the current search.

        Note: it will be applied as `boost` when `{CONFIG_PREFER_BOOST}`
        enabled and as `bf` otherwise.

        """
        return None

    def get_extra_qf(self, search_params: dict[str, Any]) -> Optional[str]:
        """Return an additional fragment of the Solr's qf.

        This fragment will be appended to the current qf
        """
        return None
