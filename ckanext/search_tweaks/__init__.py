from __future__ import annotations

from typing import Any
import ckan.plugins.toolkit as tk

CONFIG_PREFER_BOOST = "ckanext.search_tweaks.common.prefer_boost"
DEFAULT_PREFER_BOOST = True


def boost_preffered() -> bool:
    return tk.asbool(
        tk.config.get(CONFIG_PREFER_BOOST, DEFAULT_PREFER_BOOST)
    )


def feature_disabled(feature: str, search_params: dict[str, Any]) -> bool:
    return tk.asbool(
        search_params.get("extras", {}).get(
            f"ext_search_tweaks_disable_{feature}", False
        )
    )
