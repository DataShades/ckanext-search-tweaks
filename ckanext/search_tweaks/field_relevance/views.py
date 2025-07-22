from __future__ import annotations

from typing import Any

from flask import Blueprint
from flask.views import MethodView

import ckan.types as types
import ckan.model as model
import ckan.plugins.toolkit as tk

CONFIG_ENABLE_PROMOTION_ROUTE = (
    "ckanext.search_tweaks.field_relevance.blueprint.promotion.enabled"
)
CONFIG_PROMOTION_PATH = "ckanext.search_tweaks.field_relevance.blueprint.promotion.path"
CONFIG_MIN_PROMOTION = (
    "ckanext.search_tweaks.field_relevance.blueprint.promotion.min_value"
)
CONFIG_MAX_PROMOTION = (
    "ckanext.search_tweaks.field_relevance.blueprint.promotion.max_value"
)
CONFIG_PROMOTION_FIELD = (
    "ckanext.search_tweaks.field_relevance.blueprint.promotion.field_name"
)

DEFAULT_ENABLE_PROMOTION_ROUTE = False
DEFAULT_PROMOTION_PATH = "/dataset/promote/<id>"
DEFAULT_MIN_PROMOTION = 0
DEFAULT_MAX_PROMOTION = 100
DEFAULT_PROMOTION_FIELD = "promotion_level"

field_relevance = Blueprint("search_tweaks_field_relevance", __name__)


class PromoteView(MethodView):
    def _check_access(self, id: str) -> None:
        try:
            tk.check_access("search_tweaks_field_relevance_promote", {}, {"id": id})
        except tk.NotAuthorized:
            return tk.abort(403, tk._("Unauthorized to read package %s") % id)

    def post(self, id):
        self._check_access(id)
        field = tk.config.get(CONFIG_PROMOTION_FIELD, DEFAULT_PROMOTION_FIELD)
        schema = {
            field: [
                tk.get_validator("convert_int"),
                tk.get_validator("int_validator"),
                tk.get_validator("limit_to_configured_maximum")(
                    CONFIG_MAX_PROMOTION,
                    DEFAULT_MAX_PROMOTION,
                ),
            ],
        }

        data, errors = tk.navl_validate(
            dict(tk.request.form),
            schema,
            types.Context(model=model, session=model.Session),  # type: ignore
        )

        if errors:
            return self.get(id, data, errors)
        try:
            pkg_dict = tk.get_action("package_patch")(
                {},
                {"id": id, field: data[field]},
            )
        except tk.ValidationError as e:
            for k, v in e.error_summary.items():
                tk.h.flash_error(f"{k}: {v}")
            return self.get(id, data, e.error_dict)

        return tk.redirect_to("dataset.read", id=pkg_dict["name"])

    def get(
        self,
        id,
        data: dict[str, Any] | None = None,
        errors: dict[str, Any] | None = None,
    ):
        self._check_access(id)
        field = tk.config.get(CONFIG_PROMOTION_FIELD, DEFAULT_PROMOTION_FIELD)
        pkg_dict = tk.get_action("package_show")({}, {"id": id})
        extra_vars = {
            "pkg_dict": pkg_dict,
            "errors": errors or {},
            "data": data or pkg_dict,
            "min_promotion": tk.asint(
                tk.config.get(CONFIG_MIN_PROMOTION, DEFAULT_MIN_PROMOTION),
            ),
            "max_promotion": tk.asint(
                tk.config.get(CONFIG_MAX_PROMOTION, DEFAULT_MAX_PROMOTION),
            ),
            "field_name": field,
        }

        return tk.render("search_tweaks/field_relevance/promote.html", extra_vars)


if tk.asbool(
    tk.config.get(CONFIG_ENABLE_PROMOTION_ROUTE, DEFAULT_ENABLE_PROMOTION_ROUTE),
):
    field_relevance.add_url_rule(
        "/dataset/promote/<id>",
        view_func=PromoteView.as_view("promote"),
    )
