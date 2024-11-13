from __future__ import annotations

from string import Template
from typing import Any

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk

from ckanext.search_tweaks.cli import attach_relevance_command
from ckanext.search_tweaks.interfaces import ISearchTweaks
from ckanext.search_tweaks.shared import feature_disabled

from . import QueryScore, cli, normalize_query, update_score_by_url

CONFIG_BOOST_STRING = "ckanext.search_tweaks.query_relevance.boost_function"
CONFIG_RELEVANCE_PREFIX = "ckanext.search_tweaks.query_relevance.field_prefix"

DEFAULT_BOOST_STRING = "scale(def($field,0),1,1.2)"
DEFAULT_RELEVANCE_PREFIX = "query_relevance_"


class QueryRelevancePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(ISearchTweaks, inherit=True)

    # IConfigurable

    def configure(self, config):
        attach_relevance_command(cli.query)

    # IPackageController

    def before_dataset_index(self, pkg_dict):
        prefix = tk.config.get(CONFIG_RELEVANCE_PREFIX, DEFAULT_RELEVANCE_PREFIX)

        for _, query, score in QueryScore.get_for(pkg_dict["id"]):
            query = query.replace(" ", "_")
            pkg_dict[prefix + query] = score

        return pkg_dict

    def read(self, entity):
        # update search relevance only for WEB-requests. Any kind of
        # CLI/search-index manipulations has no effect on it
        if tk.request and tk.get_endpoint() == (entity.type, "read"):
            update_score_by_url(entity)

    # ISearchTweaks

    def get_search_boost_fn(self, search_params: dict[str, Any]) -> str | None:
        if feature_disabled("query_boost", search_params) or not search_params.get("q"):
            return None

        normalized = normalize_query(search_params["q"]).replace(" ", "_")
        if not normalized:
            return None

        prefix = tk.config.get(CONFIG_RELEVANCE_PREFIX, DEFAULT_RELEVANCE_PREFIX)
        field = prefix + normalized
        boost_string = Template(
            tk.config.get(CONFIG_BOOST_STRING, DEFAULT_BOOST_STRING),
        )

        return boost_string.safe_substitute({"field": field})
