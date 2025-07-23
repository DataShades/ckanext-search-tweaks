import ckan.plugins.toolkit as tk

CONF_MIN_BOOST = "ckanext.search_tweaks.query_relevance.min_boost"
CONF_MAX_BOOST = "ckanext.search_tweaks.query_relevance.max_boost"
CONF_MAX_BOOST_COUNT = "ckanext.search_tweaks.query_relevance.max_boost_count"


def get_min_boost() -> float:
    return as_float(tk.config[CONF_MIN_BOOST])


def get_max_boost() -> float:
    return as_float(tk.config[CONF_MAX_BOOST])


def get_max_boost_count() -> int:
    return tk.config[CONF_MAX_BOOST_COUNT]


def as_float(number: str) -> float:
    """Convert a string into a float.

    Example:
        assert as_float("1.5") == 1.5
    """
    try:
        return float(number)
    except (TypeError, ValueError):
        raise ValueError("Bad float value: {}".format(number))
