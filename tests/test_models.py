"""Tests for todo models."""
import pytest

from todo_cli.models import Todo, TodoStatus


def test_todo_creation():
    """Test creating a todo."""
    todo = Todo(id=1, title="Test todo")
    assert todo.id == 1
    assert todo.title == "Test todo"
    assert todo.description is None
    assert todo.status == TodoStatus.PENDING


def test_todo_with_description():
    """Test todo with description."""
    todo = Todo(id=1, title="Test", description="Test description")
    assert todo.description == "Test description"


def test_todo_to_dict():
    """Test converting todo to dictionary."""
    todo = Todo(id=1, title="Test", description="Desc", status=TodoStatus.DONE)
    data = todo.to_dict()
    assert data == {
        "id": 1,
        "title": "Test",
        "description": "Desc",
        "status": "done",
        "created_at": todo.created_at,
    }


def test_todo_from_dict():
    """Test creating todo from dictionary."""
    data = {
        "id": 1,
        "title": "Test",
        "description": "Desc",
        "status": "done",
        "created_at": "2025-12-30T00:00:00",
    }
    todo = Todo.from_dict(data)
    assert todo.id == 1
    assert todo.title == "Test"
    assert todo.description == "Desc"
    assert todo.status == TodoStatus.DONE
