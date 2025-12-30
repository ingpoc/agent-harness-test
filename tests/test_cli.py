"""Tests for CLI commands."""
import pytest
from typer.testing import CliRunner

from todo_cli.cli import app
from todo_cli.storage import TodoStorage

runner = CliRunner()


@pytest.fixture
def temp_storage(tmp_path, monkeypatch):
    """Create temporary storage and patch storage location."""
    filepath = tmp_path / "test_todos.json"
    monkeypatch.setattr("todo_cli.cli.TodoStorage", lambda: TodoStorage(str(filepath)))
    return TodoStorage(str(filepath))


def test_add_todo(temp_storage, capsys):
    """Test adding a todo via CLI."""
    result = runner.invoke(app, ["add", "Test todo"])
    assert result.exit_code == 0
    assert "Todo created" in result.stdout

    todos = temp_storage.get_all()
    assert len(todos) == 1
    assert todos[0].title == "Test todo"


def test_add_todo_with_description(temp_storage):
    """Test adding a todo with description."""
    result = runner.invoke(app, ["add", "Test todo", "--description", "Test description"])
    assert result.exit_code == 0

    todo = temp_storage.get_by_id(1)
    assert todo.description == "Test description"


def test_list_todos(temp_storage):
    """Test listing todos."""
    temp_storage.create("First todo")
    temp_storage.create("Second todo")

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "First todo" in result.stdout
    assert "Second todo" in result.stdout


def test_list_empty(temp_storage):
    """Test listing when no todos."""
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "No todos found" in result.stdout


def test_list_by_status(temp_storage):
    """Test filtering todos by status."""
    t1 = temp_storage.create("Pending todo")
    t2 = temp_storage.create("Done todo")
    temp_storage.update(t2.id, status="done")

    result = runner.invoke(app, ["list", "--status", "pending"])
    assert result.exit_code == 0
    assert "Pending todo" in result.stdout
    assert "Done todo" not in result.stdout


def test_complete_todo(temp_storage):
    """Test marking a todo as complete."""
    todo = temp_storage.create("Test todo")
    assert todo.status == "pending"

    result = runner.invoke(app, ["complete", str(todo.id)])
    assert result.exit_code == 0
    assert "marked as done" in result.stdout

    updated = temp_storage.get_by_id(todo.id)
    assert updated.status == "done"


def test_complete_nonexistent(temp_storage):
    """Test completing a todo that doesn't exist."""
    result = runner.invoke(app, ["complete", "999"])
    assert result.exit_code == 1
    assert "not found" in result.stdout


def test_delete_todo(temp_storage):
    """Test deleting a todo."""
    todo = temp_storage.create("To delete")
    assert temp_storage.get_by_id(todo.id) is not None

    result = runner.invoke(app, ["delete", str(todo.id)])
    assert result.exit_code == 0
    assert "deleted" in result.stdout

    assert temp_storage.get_by_id(todo.id) is None


def test_delete_nonexistent(temp_storage):
    """Test deleting a todo that doesn't exist."""
    result = runner.invoke(app, ["delete", "999"])
    assert result.exit_code == 1
    assert "not found" in result.stdout


def test_cli_help():
    """Test CLI help output."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "add" in result.stdout
    assert "list" in result.stdout
    assert "complete" in result.stdout
    assert "delete" in result.stdout
