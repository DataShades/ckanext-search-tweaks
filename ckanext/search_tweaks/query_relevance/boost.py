from __future__ import annotations

from ckanext.search_tweaks.config import prefer_boost

from . import QueryScore
from .config import get_min_boost, get_max_boost, get_max_boost_count


def build_boost_query_function(search_query: str) -> str | None:
    """Build boost query function for given search query.

    Args:
        search_query: normalized query

    Returns:
        Boost function
    """
    boosts, max_score = get_boost_values(search_query)
    min_boost = get_min_boost()
    max_boost = get_max_boost()

    if prefer_boost():
        boost_expr = "1"

        for pkg_id, raw_score in sorted(boosts.items(), reverse=True):
            scaled = scale_score(raw_score, max_score, min_boost, max_boost)
            boost_expr = f'if(eq(id,"{pkg_id}"),{scaled},{boost_expr})'

        return f"sum(0, {boost_expr})"
    else:
        boost_parts = []

        for pkg_id, raw_score in boosts.items():
            score = scale_score(raw_score, max_score, min_boost, max_boost)

            boost_parts.append(f'if(eq(id,"{pkg_id}"),{score},0)')

        return f"sum(1,{','.join(boost_parts)})"


def get_boost_values(search_query: str) -> tuple[dict[str, float], float]:
    boosts = {}
    max_score = 0

    for entry in QueryScore.get_for_query(search_query):
        package_id, score = entry

        if score > max_score:
            max_score = score

        boosts[package_id.decode("utf-8")] = score

    return boosts, max_score


def scale_score(
    value: float,
    max_value: float,
    min_boost: float,
    max_boost: float,
) -> float:
    """
    Linearly scales a value to the range [min_boost, max_boost].

    This prevents datasets with high scores
    from overpowering search relevance, ensuring more balanced results.
    """
    if max_value == 0:
        return min_boost

    value = max(0, min(value, max_value))

    scaled = min_boost + (value / max_value) * (max_boost - min_boost)

    return round(scaled, 4)
