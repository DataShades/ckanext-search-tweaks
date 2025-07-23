from __future__ import annotations

from typing import Any

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk

from ckanext.search_tweaks.cli import attach_relevance_command
from ckanext.search_tweaks.interfaces import ISearchTweaks
from ckanext.search_tweaks.shared import feature_disabled

from . import cli, normalize_query, update_score_by_url
from .boost import build_boost_query_function


@tk.blanket.config_declarations
class QueryRelevancePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(ISearchTweaks, inherit=True)

    # IConfigurable

    def configure(self, config):
        attach_relevance_command(cli.query)

    # IPackageController

    def read(self, entity):
        # update search relevance only for WEB-requests. Any kind of
        # CLI/search-index manipulations has no effect on it
        if tk.request and tk.get_endpoint() == (entity.type, "read"):
            update_score_by_url(entity)

    # ISearchTweaks

    def get_search_boost_fn(self, search_params: dict[str, Any]) -> str | None:
        q = search_params.get("q")

        if feature_disabled("query_boost", search_params) or not q:
            return None

        if normalized := normalize_query(q).replace(" ", "_"):
            return build_boost_query_function(normalized)

        return None
