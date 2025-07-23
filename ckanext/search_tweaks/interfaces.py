from __future__ import annotations

from typing import Any

from ckan.plugins.interfaces import Interface


class ISearchTweaks(Interface):
    def get_search_boost_fn(self, search_params: dict[str, Any]) -> str | None:
        """Return Solr's boost function applicable to the current search.

        Note: it will be applied as `boost` when
        `ckanext.search_tweaks.common.prefer_boost` enabled and as `bf`
        otherwise.

        """
        return None

    def get_extra_qf(self, search_params: dict[str, Any]) -> str | None:
        """Return an additional fragment of the Solr's qf.

        This fragment will be appended to the current qf
        """
        return None


class IQueryPopularity(Interface):
    def skip_query_popularity(self, params: dict[str, Any]) -> bool:
        """Do not index search query."""
        return False
