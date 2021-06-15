import datetime
import csv
from ckan.lib.redis import connect_to_redis

import click
import freezegun
import ckan.model as model

from ckanext.search_tweaks.query_relevance import QueryScore

def get_commands():
    return [search_tweaks]


@click.group(short_help="Search tweaks")
def search_tweaks():
    pass

@click.group(short_help="Manage search relevance")
def relevance():
    pass

_search_csv_headers = ["package_id", "search_query", "count_of_hits"]

@click.group(short_help="Manage search relevance")
def query():
    pass

# TODO: move to the plugin's update_config
relevance.add_command(query)

@query.command("import")
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
    click.secho("Done", fg="green")

@query.command()
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
    click.secho("Done", fg="green")


@query.command()
def align():
    """Remove old records.
    """
    rows = QueryScore.get_all()
    for (id_, query, _) in rows:
        score = QueryScore(id_, query)
        score.align()

@query.command()
@click.option("--days", "-d", type=int, default=1)
@click.argument("file")
@click.pass_context
def safe_export(ctx, days, file):
    conn = connect_to_redis()
    uptime = conn.info()["uptime_in_days"]
    if uptime >= days:
        click.secho(f"Redis runs for {uptime} days. Creating snapshot..", fg="green")
        ctx.invoke(export, output=click.File("w")(file))
    else:
        click.secho(f"Redis runs for {uptime} days. Restore stats from snapshot..", fg="red")
        ctx.invoke(import_source, source=click.File()(file))
