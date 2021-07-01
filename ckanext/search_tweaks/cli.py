import click


def get_commands():
    return [search_tweaks]


@click.group(short_help="Search tweaks")
def search_tweaks():
    pass


@search_tweaks.group(short_help="Manage search relevance")
def relevance():
    pass


attach_main_command = search_tweaks.add_command
attach_relevance_command = relevance.add_command
