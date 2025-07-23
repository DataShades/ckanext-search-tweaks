from __future__ import annotations

import csv
import datetime
import logging
from typing import TextIO

import click
import freezegun

import ckan.model as model

from . import QueryScore


log = logging.getLogger(__name__)


@click.group(short_help="Manage search relevance")
def query():
    pass


@query.command("import")
@click.argument("source", type=click.File())
@click.option("--date", type=datetime.date.fromisoformat)
def import_source(source: TextIO, date) -> None:
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
def export(output: TextIO | None) -> None:
    """Export search stats into specified file."""
    rows = QueryScore.get_all()

    if output:
        writer = csv.writer(output)
        writer.writerow(["package_id", "search_query", "count_of_hits"])
        writer.writerows(rows)
    else:
        for row in rows:
            click.echo("ID: {}, query: {}, count: {}".format(*row))

    click.secho("Done", fg="green")


@query.command()
def reset() -> None:
    """Reset query relevance scores"""
    QueryScore.reset_all()

    click.secho("Done", fg="green")
