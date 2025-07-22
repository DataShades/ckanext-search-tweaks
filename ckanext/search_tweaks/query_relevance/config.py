import ckan.plugins.toolkit as tk

CONF_MIN_BOOST = "ckanext.search_tweaks.query_relevance.min_boost"
CONF_MAX_BOOST = "ckanext.search_tweaks.query_relevance.max_boost"
CONF_MAX_BOOST_COUNT = "ckanext.search_tweaks.query_relevance.max_boost_count"
CONF_STORE_BACKEND = "ckanext.search_tweaks.query_relevance.backend"
CONF_DAILY_AGE = "ckanext.search_tweaks.query_relevance.daily.age"


def get_min_boost() -> float:
    return as_float(tk.config[CONF_MIN_BOOST])


def get_max_boost() -> float:
    return as_float(tk.config[CONF_MAX_BOOST])


def get_max_boost_count() -> int:
    return tk.config[CONF_MAX_BOOST_COUNT]


def get_store_backend() -> str:
    return tk.config[CONF_STORE_BACKEND]


def get_daily_age() -> int:
    return tk.config[CONF_DAILY_AGE]


def as_float(number: str) -> float:
    """Convert a string into a float.

    Example:
        assert as_float("1.5") == 1.5
    """
    try:
        return float(number)
    except (TypeError, ValueError):
        raise ValueError("Bad float value: {}".format(number))
