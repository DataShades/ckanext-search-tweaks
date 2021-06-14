import ckan.plugins as plugins

from . import cli
from .interfaces import ISearchBoost

class SearchTweaksPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IClick

    def get_commands(self):
        return cli.get_commands()

    # IPackageController

    def before_search(self, search_params):
        if "defType" not in search_params:
            search_params["defType"] = "edismax"

        bf = search_params.get("bf") or "0"
        for plugin in plugins.PluginImplementations(ISearchBoost):
            extra_bf = plugin.get_search_boost_fn(search_params)
            if not extra_bf:
                continue
            bf = f"sum({bf},{extra_bf})"
        search_params["bf"] = bf

        return search_params
