from __future__ import annotations
import contextlib

from urllib.parse import urlparse, parse_qs

from werkzeug.routing import BuildError

import ckan.plugins.toolkit as tk
import ckan.model as model

from .score import QueryScore, normalize_query

__all__ = ["QueryScore", "normalize_query", "update_score_by_url"]


def update_score_by_url(pkg: model.Package, referrer: str | None = None) -> bool:
    """Boost the relevance of the given package for the current search query

    Args:
        pkg: the package to boost
        referrer: the URL of the current request

    Returns:
        True if the package was boosted, False otherwise
    """

    referrer = referrer or (tk.request.referrer if tk.request else None)

    if not referrer:
        return False

    url = urlparse(referrer)

    if not _is_scoring_enabled_for_path(url.path, pkg):
        return False

    query = parse_qs(url.query.lstrip("?"))

    if "q" not in query:
        return False

    QueryScore(pkg.id, query["q"][0]).increase(1)

    return True


def _is_scoring_enabled_for_path(path: str, package: model.Package) -> bool:
    """
    Determine if a given URL path should have scoring enabled.

    Checks if the provided path matches any of the following URL patterns that
    support scoring functionality:

    Args:
        path: The URL path to check
        package: The package object containing type and owner_org info

    Returns:
        True if the path should have scoring enabled, False otherwise
    """

    path = path.rstrip("/")

    if path == tk.h.url_for("dataset.search").rstrip("/"):
        return True

    with contextlib.suppress(BuildError):
        if path == tk.h.url_for(package.type + ".search").rstrip("/"):
            return True

    org = model.Group.get(package.owner_org)

    if not org:
        return False

    if path == tk.h.url_for("organization.read", id=org.name):
        return True

    with contextlib.suppress(BuildError):
        if path == tk.h.url_for(org.type + ".read", id=org.name):
            return True

    return False
