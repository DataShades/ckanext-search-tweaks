import csv
import datetime

import click
import freezegun

import ckan.model as model
from ckan.lib.redis import connect_to_redis

from . import QueryScore

_search_csv_headers = ["package_id", "search_query", "count_of_hits"]


@click.group(short_help="Manage search relevance")
def query():
    pass


@query.command("import")
@click.argument("source", type=click.File())
@click.option("--date", type=datetime.date.fromisoformat)
def import_source(source, date):
    """Import search stats from source"""
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
    """Export search stats into specified file."""
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
    """Remove old records."""
    rows = QueryScore.get_all()
    for (id_, query, _) in rows:
        score = QueryScore(id_, query)
        score.align()


@query.command()
@click.option("--days", "-d", type=int, default=1)
@click.argument("file")
@click.pass_context
def safe_export(ctx, days, file):
    """Export stats if redis haven't been reloaded recently.

    If redis runs less than N days, it was reloaded recently and contains no
    stats. We have to import old snapshot into it.

    If redis is up for N days and more, it contains relevant stats. We can
    safely export them and overwrite old snapshot.

    """
    conn = connect_to_redis()
    uptime = conn.info()["uptime_in_days"]
    if uptime >= days:
        click.secho(f"Redis runs for {uptime} days. Creating snapshot..", fg="green")
        ctx.invoke(export, output=click.File("w")(file))
    else:
        click.secho(
            f"Redis runs for {uptime} days. Restore stats from snapshot..", fg="red"
        )
        ctx.invoke(import_source, source=click.File()(file))
