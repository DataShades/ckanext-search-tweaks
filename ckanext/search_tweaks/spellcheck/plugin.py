import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ..cli import attach_main_command
from . import cli, helpers


class SpellcheckPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurable)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    # IConfigurable

    def configure(self, config):
        attach_main_command(cli.spellcheck)

    # IConfigurer

    def update_config(self, config):
        tk.add_template_directory(config, "templates")

    # ITemplateHelpers

    def get_helpers(self):
        return helpers.get_helpers()
