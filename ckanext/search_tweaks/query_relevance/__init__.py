from __future__ import annotations
import contextlib
from typing import Optional

from urllib.parse import urlparse, parse_qs

from werkzeug.routing import BuildError

import ckan.plugins.toolkit as tk
import ckan.model as model

from .score import QueryScore, normalize_query

__all__ = ["QueryScore", "normalize_query", "update_score_by_url"]


def update_score_by_url(pkg: model.Package, ref: Optional[str] = None) -> bool:
    """Make given package more relevant for the current search query."""
    if tk.request:
        ref = ref or tk.request.referrer

    if not ref:
        return False

    url = urlparse(ref)
    if not _path_has_score_for(url.path, pkg):
        return False

    query = parse_qs(url.query.lstrip("?"))
    if "q" not in query:
        return False
    q = query["q"][0]

    score = QueryScore(pkg.id, q)
    score.increase(1)
    return True


def _path_has_score_for(path: str, pkg: model.Package) -> bool:
    path = path.rstrip("/")
    if path == tk.h.url_for("dataset.search").rstrip("/"):
        return True

    with contextlib.suppress(BuildError):
        if path == tk.h.url_for(pkg.type + ".search").rstrip("/"):
            return True

    org = model.Group.get(pkg.owner_org)
    if not org:
        return False

    if path == tk.h.url_for("organization.read", id=org.name):
        return True

    with contextlib.suppress(BuildError):
        if path == tk.h.url_for(org.type + ".read", id=org.name):
            return True

    return False
