from __future__ import annotations

import click

from . import __version__
from .db import migrate, session


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli():
    """Habit Tracker CLI"""


@cli.command("init-db")
def init_db():
    with session() as conn:
        migrate(conn)
    click.echo("Database initialised (habit_tracker.db).")


@cli.command()
def version():
    click.echo(__version__)


if __name__ == "__main__":
    cli()
