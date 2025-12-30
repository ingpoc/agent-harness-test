"""Tests for CLI commands."""

from typer.testing import CliRunner

from todo_cli.cli import app

runner = CliRunner()


def test_add_command() -> None:
    """Test the add command."""
    result = runner.invoke(app, ["add", "Test todo"])
    assert result.exit_code == 0
    assert "Test todo" in result.stdout


def test_list_command() -> None:
    """Test the list command."""
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "YOUR TODOS" in result.stdout


def test_complete_command() -> None:
    """Test the complete command."""
    result = runner.invoke(app, ["complete", "F-001"])
    assert result.exit_code == 0
    assert "F-001" in result.stdout


def test_delete_command() -> None:
    """Test the delete command."""
    result = runner.invoke(app, ["delete", "F-001"])
    assert result.exit_code == 0
    assert "F-001" in result.stdout
