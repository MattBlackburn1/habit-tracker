from __future__ import annotations

import sys

import click

from . import __version__
from .db import migrate, session
from .models import create_habit, get_habit_by_name, list_habit


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli():
    """Habit Tracker CLI"""
    pass


@cli.command("add")
@click.argument("name")
@click.option("--freq")
def add_cmd(name, freq):
    with session() as conn:
        name = name.strip()
        freq = freq.lower()

        habit = get_habit_by_name(conn, name)
        if habit:
            click.echo(f"Habit {name} already exists", err=True)
            sys.exit(1)

        new_habit = create_habit(conn, name=name, frequency=freq)
        click.echo(f'Added Habit #{new_habit.id}: "{new_habit.name}" [{new_habit.frequency}]')


@cli.command("list")
@click.option("--all", "show_all", is_flag=True, help="Include inactive habits")
def list_cmd(show_all):
    with session() as conn:
        migrate(conn)
        habits = list_habit(conn, include_inactive=show_all)
        if not habits:
            click.echo("No habits yet. Add one with: cli add 'NAME' --freq daily")
            return
        for h in habits:
            id_str = f"{h.id:>3}"

            line = f"{id_str} {h.name} {h.frequency} created: {h.created_at}"

            if not h.is_active:
                line += "(inactive)"

            click.echo(line)


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
