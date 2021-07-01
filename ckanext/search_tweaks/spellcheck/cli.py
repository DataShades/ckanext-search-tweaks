import click

@click.group(short_help="Manage search suggestions")
def spellcheck():
    pass


@spellcheck.command("rebuild")
def rebuild_suggestions():
    from ckanext.search_tweaks.spellcheck.plugin import rebuild_dictionary

    rebuild_dictionary()
    click.secho("Done", fg="green")
