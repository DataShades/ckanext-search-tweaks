from __future__ import annotations

from typing import Any

import ckan.plugins as p
import ckan.plugins.toolkit as tk

from ckanext.search_tweaks.interfaces import IQueryPopularity

from . import config, score


@tk.blanket.actions
@tk.blanket.auth_functions
@tk.blanket.config_declarations
class QueryPopularityPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurable)
    p.implements(p.IPackageController, inherit=True)
    p.implements(IQueryPopularity, inherit=True)

    def after_dataset_search(self, results: dict[str, Any], params: dict[str, Any]):
        bp, view = tk.get_endpoint()
        if (
            bp
            and view
            and f"{bp}.{view}" in config.tracked_endpoints()
            and not any(
                plugin.skip_query_popularity(params)
                for plugin in p.PluginImplementations(IQueryPopularity)
            )
        ):
            self.score.hit(params["q"].strip())

        return results

    def configure(self, config: Any):
        self.score = score.Score()

    def skip_query_popularity(self, params: dict[str, Any]) -> bool:
        q = params["q"]

        if q == "*:*":
            return config.skip_irrefutable()

        symbols = config.ignored_symbols()
        if symbols and set(q) & symbols:
            return True

        terms = config.ignored_terms()

        return any(term in q for term in terms)
