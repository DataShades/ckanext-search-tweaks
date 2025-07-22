from __future__ import annotations

import json
from typing import Any

from ckan import types
import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ckan.exceptions import CkanConfigurationException

CONFIG_FORM_DEFINITION = "ckanext.search_tweaks.advanced_search.fields"
CONFIG_FIELD_ORDER = "ckanext.search_tweaks.advanced_search.order"

DEFAULT_FORM_DEFINITION = json.dumps(
    {
        "text": {
            "type": "text",
            "label": "Any listed item",
            "placeholder": "Enter a search term",
            "default": True,
        },
        "title": {
            "type": "text",
            "label": "Title",
            "placeholder": "Enter a search term",
        },
        "notes": {
            "type": "text",
            "label": "Description",
            "placeholder": "Enter a search term",
        },
        "capacity": {
            "type": "select",
            "label": "Visibility",
            "placeholder": "Filter data by visibility",
            "options": [
                {"value": "public", "label": "Public"},
                {"value": "private", "label": "Private"},
            ],
        },
    },
)
DEFAULT_FIELD_ORDER = None


def form_config():
    definition = json.loads(
        tk.config.get(CONFIG_FORM_DEFINITION, DEFAULT_FORM_DEFINITION),
    )
    order = tk.aslist(tk.config.get(CONFIG_FIELD_ORDER, DEFAULT_FIELD_ORDER))
    if not order:
        order = list(definition)
    return {
        "definitions": definition,
        "order": order,
    }


@tk.side_effect_free
def advanced_search_config(
    context: types.Context,
    data_dict: dict[str, Any],
) -> dict[str, Any]:
    """Configuration for advanced search fields."""
    return tk.h.advanced_search_form_config()


@tk.blanket.actions({"advanced_search_config": advanced_search_config})
class AdvancedSearchPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IConfigurable)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IPackageController, inherit=True)

    # IConfigurer

    def update_config(self, config):
        tk.add_template_directory(config, "templates")
        tk.add_resource("assets", "search_tweaks_advanced_search")

    # IConfigurable

    def configure(self, config):
        try:
            from ckanext.composite_search.interfaces import ICompositeSearch
        except ImportError as err:
            msg = "ckanext-composite-search is not installed"
            raise CkanConfigurationException(msg) from err

        if not p.plugin_loaded("composite_search"):
            msg = "Advanced search requires `composite_search` plugin"
            raise CkanConfigurationException(msg)
        if not list(p.PluginImplementations(ICompositeSearch)):
            msg = (
                "Advanced search requires plugin that implements"
                + " ICompositeSearch. Consider enabling "
                + "`default_composite_search` plugins."
            )
            raise CkanConfigurationException(msg)

    # ITemplateHelpers

    def get_helpers(self):
        return {
            "advanced_search_form_config": form_config,
        }

    # IPackageController

    def before_dataset_search(self, search_params: dict[str, Any]):
        solr_q = search_params.get("extras", {}).get("ext_solr_q", None)
        if solr_q:
            search_params.setdefault("q", "")
            search_params["q"] += " " + solr_q
        return search_params

    if not tk.check_ckan_version("2.10"):
        before_search = before_dataset_search
