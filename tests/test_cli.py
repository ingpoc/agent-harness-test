"""Tests for CLI commands and storage."""

import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from typer.testing import CliRunner

from todo_cli.cli import app
from todo_cli.models import Status, Todo
from todo_cli.storage import TodoStorage

runner = CliRunner()


class TestTodoStorage:
    """Test TodoStorage class."""

    def setup_method(self) -> None:
        """Create temporary storage file for each test."""
        self.temp_file = Path(NamedTemporaryFile(mode="w", delete=False, suffix=".json").name)
        self.storage = TodoStorage(file_path=self.temp_file)

    def teardown_method(self) -> None:
        """Clean up temporary file."""
        if self.temp_file.exists():
            self.temp_file.unlink()

    def test_add_todo_generates_semantic_id(self) -> None:
        """Test that adding a todo generates semantic ID (F-001, F-002)."""
        todo1 = Todo(title="First todo")
        created1 = self.storage.add(todo1)
        assert created1.id == "F-001"

        todo2 = Todo(title="Second todo")
        created2 = self.storage.add(todo2)
        assert created2.id == "F-002"

    def test_list_all_todos(self) -> None:
        """Test listing all todos."""
        self.storage.add(Todo(title="Todo 1"))
        self.storage.add(Todo(title="Todo 2"))

        todos = self.storage.list_all()
        assert len(todos) == 2
        assert todos[0].title == "Todo 1"
        assert todos[1].title == "Todo 2"

    def test_get_todo_by_id(self) -> None:
        """Test getting a todo by ID."""
        created = self.storage.add(Todo(title="Find me"))
        found = self.storage.get(created.id)

        assert found is not None
        assert found.title == "Find me"
        assert found.id == created.id

    def test_update_todo_status(self) -> None:
        """Test updating todo status to done."""
        created = self.storage.add(Todo(title="Complete me"))
        assert created.status == Status.PENDING

        updated = self.storage.update(created.id, status=Status.DONE)
        assert updated is not None
        assert updated.status == Status.DONE

    def test_delete_todo(self) -> None:
        """Test deleting a todo."""
        created = self.storage.add(Todo(title="Delete me"))

        assert self.storage.delete(created.id) is True
        assert self.storage.get(created.id) is None

    def test_filter_by_status(self) -> None:
        """Test filtering todos by status."""
        self.storage.add(Todo(title="Pending 1"))
        todo2 = self.storage.add(Todo(title="Done task"))
        self.storage.update(todo2.id, status=Status.DONE)

        pending = self.storage.filter_by_status(Status.PENDING)
        done = self.storage.filter_by_status(Status.DONE)

        assert len(pending) == 1
        assert len(done) == 1
        assert pending[0].title == "Pending 1"
        assert done[0].title == "Done task"


class TestCLI:
    """Test CLI commands."""

    def test_add_command(self) -> None:
        """Test the add command."""
        result = runner.invoke(app, ["add", "Test todo"])
        assert result.exit_code == 0
        assert "Test todo" in result.stdout

    def test_list_command(self) -> None:
        """Test the list command."""
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "YOUR TODOS" in result.stdout

    def test_complete_command(self) -> None:
        """Test the complete command."""
        # First add a todo
        runner.invoke(app, ["add", "To complete"])
        # Then complete F-001
        result = runner.invoke(app, ["complete", "F-001"])
        assert result.exit_code == 0

    def test_delete_command(self) -> None:
        """Test the delete command."""
        result = runner.invoke(app, ["delete", "F-001"])
        assert result.exit_code == 0

    def test_list_with_status_filter(self) -> None:
        """Test list command with status filter."""
        result = runner.invoke(app, ["list", "--status", "pending"])
        assert result.exit_code == 0
