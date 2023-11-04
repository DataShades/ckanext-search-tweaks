from __future__ import annotations
import ckan.plugins.toolkit as tk


def skip_irrefutable() -> bool:
    return tk.config["ckanext.search_tweaks.query_popularity.skip_irrefutable_search"]


def ignored_symbols() -> set[str]:
    return set(tk.config["ckanext.search_tweaks.query_popularity.ignored_symbols"])


def ignored_terms() -> list[str]:
    return tk.config["ckanext.search_tweaks.query_popularity.ignored_terms"]


def throttle() -> int:
    return tk.config["ckanext.search_tweaks.query_popularity.query_throttle"]


def max_age() -> int:
    return tk.config["ckanext.search_tweaks.query_popularity.max_age"]


def obsoletion_period() -> int:
    return tk.config["ckanext.search_tweaks.query_popularity.obsoletion_period"]


def tracked_endpoints() -> list[str]:
    return tk.config["ckanext.search_tweaks.query_popularity.tracked_endpoints"]
