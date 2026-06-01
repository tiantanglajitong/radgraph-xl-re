"""Command-line entry point for the local RadGraph-XL project."""

from __future__ import annotations

import json

import typer

from radgraph_re import __version__

app = typer.Typer(
    help="Utilities for the RadGraph-XL entity and relation extraction project.",
    no_args_is_help=True,
)


@app.callback()
def root() -> None:
    """Run RadGraph-XL project utilities."""


@app.command()
def info() -> None:
    """Print non-sensitive project metadata."""
    typer.echo(
        json.dumps(
            {
                "project": "radgraph-xl-re",
                "version": __version__,
                "status": "initialized",
            },
            indent=2,
        )
    )


def main() -> None:
    """Run the CLI."""
    app()


if __name__ == "__main__":
    main()
