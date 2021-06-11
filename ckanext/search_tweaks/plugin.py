from string import Template
import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
import ckanext.search_tweaks.relevance as relevance

from . import cli

CONFIG_BOOST_STRING = "ckanext.search_tweaks.relevance.boost_function"
CONFIG_RELEVANCE_PREFIX = "ckanext.search_tweaks.relevance.field_prefix"

DEFAULT_BOOST_STRING = "scale(def($field,0),0,2)"
DEFAULT_RELEVANCE_PREFIX = "query_relevance_"

class SearchTweaksPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IClick)

    def get_commands(self):
        return cli.get_commands()


class SearchTweaksRelevancePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurable

    def configure(self, config):
        cli.search_tweaks.add_command(cli.relevance)

    # IPackageController

    def before_index(self, pkg_dict):
        prefix = tk.config.get(CONFIG_RELEVANCE_PREFIX, DEFAULT_RELEVANCE_PREFIX)
        for (_, query, score) in relevance.QueryScore.get_for(pkg_dict["id"]):
            query = query.replace(" ", "_")
            pkg_dict[prefix + query] = score
        return pkg_dict

    def before_search(self, search_params):
        prefix = tk.config.get(CONFIG_RELEVANCE_PREFIX, DEFAULT_RELEVANCE_PREFIX)
        if "q" in search_params:
            bf = search_params.get("bf") or "0"
            field = prefix + relevance.normalize_query(search_params["q"]).replace(" ", "_")
            boost_string = Template(tk.config.get(CONFIG_BOOST_STRING, DEFAULT_BOOST_STRING))
            boost_function = boost_string.safe_substitute({"field": field})
            search_params['bf'] = f"sum({bf},{boost_function})"
        return search_params

    def read(self, entity):
        # update search relevance only for WEB-requests. Any kind of
        # CLI/search-index manipulations has no effect on it
        if tk.request and  tk.get_endpoint() == (entity.type, "read"):
            relevance.update_score_by_url(entity)
