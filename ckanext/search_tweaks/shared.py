from __future__ import annotations

from typing import Any
import ckan.plugins.toolkit as tk


def feature_disabled(feature: str, search_params: dict[str, Any]) -> bool:
    return tk.asbool(
        search_params.get("extras", {}).get(
            f"ext_search_tweaks_disable_{feature}",
            False,
        ),
    )
