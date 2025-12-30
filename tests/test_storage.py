"""Tests for todo storage."""
import pytest
from pathlib import Path

from todo_cli.models import TodoStatus
from todo_cli.storage import TodoStorage


@pytest.fixture
def temp_storage(tmp_path):
    """Create a temporary storage instance."""
    filepath = tmp_path / "todos.json"
    return TodoStorage(str(filepath))


def test_storage_creates_file(temp_storage):
    """Test that storage file is created."""
    assert temp_storage.filepath.exists()


def test_create_todo(temp_storage):
    """Test creating a todo."""
    todo = temp_storage.create("Test todo", "Test description")
    assert todo.id == 1
    assert todo.title == "Test todo"
    assert todo.description == "Test description"


def test_get_all_todos(temp_storage):
    """Test getting all todos."""
    temp_storage.create("First")
    temp_storage.create("Second")
    todos = temp_storage.get_all()
    assert len(todos) == 2
    assert todos[0].title == "First"
    assert todos[1].title == "Second"


def test_get_by_status(temp_storage):
    """Test filtering todos by status."""
    temp_storage.create("Pending todo")
    todo = temp_storage.create("Done todo")
    temp_storage.update(todo.id, status=TodoStatus.DONE)

    pending = temp_storage.get_all(status=TodoStatus.PENDING)
    done = temp_storage.get_all(status=TodoStatus.DONE)

    assert len(pending) == 1
    assert len(done) == 1
    assert pending[0].title == "Pending todo"
    assert done[0].title == "Done todo"


def test_get_by_id(temp_storage):
    """Test getting todo by ID."""
    created = temp_storage.create("Test todo")
    found = temp_storage.get_by_id(created.id)
    assert found is not None
    assert found.title == "Test todo"


def test_get_by_id_not_found(temp_storage):
    """Test getting non-existent todo."""
    found = temp_storage.get_by_id(999)
    assert found is None


def test_update_todo(temp_storage):
    """Test updating a todo."""
    todo = temp_storage.create("Original title")
    updated = temp_storage.update(todo.id, title="Updated title", status=TodoStatus.DONE)
    assert updated.title == "Updated title"
    assert updated.status == TodoStatus.DONE


def test_delete_todo(temp_storage):
    """Test deleting a todo."""
    todo = temp_storage.create("To delete")
    result = temp_storage.delete(todo.id)
    assert result is True

    todos = temp_storage.get_all()
    assert len(todos) == 0


def test_delete_todo_not_found(temp_storage):
    """Test deleting non-existent todo."""
    result = temp_storage.delete(999)
    assert result is False


def test_auto_increment_id(temp_storage):
    """Test that IDs auto-increment."""
    t1 = temp_storage.create("First")
    t2 = temp_storage.create("Second")
    t3 = temp_storage.create("Third")
    assert t1.id == 1
    assert t2.id == 2
    assert t3.id == 3
