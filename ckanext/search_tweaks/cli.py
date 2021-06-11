import datetime
import csv

import click
import freezegun
import ckan.model as model

from ckanext.search_tweaks.relevance import QueryScore

def get_commands():
    return [search_tweaks]


@click.group(short_help="Search tweaks")
def search_tweaks():
    pass

@click.group(short_help="Manage search relevance")
def relevance():
    pass

_search_csv_headers = ["package_id", "search_query", "count_of_hits"]

@relevance.command("import")
@click.argument("source", type=click.File())
@click.option("--date", type=datetime.date.fromisoformat)
def import_source(source, date):
    """Import search stats from source
    """
    if not date:
        date = datetime.date.today()
    with freezegun.freeze_time(date):
        reader = csv.DictReader(source)
        for row in reader:
            pkg = model.Package.get(row["package_id"])
            if not pkg:
                click.secho(f"Package {row['package_id']} does not exists", fg="red")
                continue
            score = QueryScore(pkg.id, row["search_query"])
            score.reset()
            score.increase(int(row["count_of_hits"]))


@relevance.command()
@click.argument("output", type=click.File("w"), required=False)
def export(output):
    """Export search stats into specified file.
    """
    rows = QueryScore.get_all()
    if output:
        writer = csv.writer(output)
        writer.writerow(_search_csv_headers)
        writer.writerows(rows)
    else:
        for row in rows:
            click.echo("Id: %s, query: %s, count: %d" % row)


@relevance.command()
def align():
    """Remove old records.
    """
    rows = QueryScore.get_all()
    for (id_, query, _) in rows:
        score = QueryScore(id_, query)
        score.align()
