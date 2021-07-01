import click

from . import rebuild_dictionary


@click.group(short_help="Manage search suggestions")
def spellcheck():
    pass


@spellcheck.command("rebuild")
def rebuild_suggestions():
    rebuild_dictionary()
    click.secho("Done", fg="green")
