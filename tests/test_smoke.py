from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from radgraph_re import __version__
from radgraph_re.cli import app


def test_package_version() -> None:
    assert __version__ == "0.1.0"


def test_info_command() -> None:
    result = CliRunner().invoke(app, ["info"])

    assert result.exit_code == 0
    assert '"project": "radgraph-xl-re"' in result.stdout
    assert '"status": "initialized"' in result.stdout


def test_gitignore_excludes_restricted_artifacts() -> None:
    gitignore = (Path(__file__).parents[1] / ".gitignore").read_text(
        encoding="utf-8"
    )

    for required_pattern in (".env", "*.zip", "*.jsonl", "data/", "outputs/"):
        assert required_pattern in gitignore

