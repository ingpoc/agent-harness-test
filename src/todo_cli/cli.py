"""CLI Todo App - Main entry point with distinctive terminal design.

Aesthetic: Minimalist Zen
- Palette: Nord-inspired cool blues on dark gray
- Borders: Rounded (╭─╮│╰╯)
- Status symbols: ▸ pending, ✓ done, ○ empty
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from todo_cli.models import Status, Todo
from todo_cli.storage import TodoStorage

app = typer.Typer(
    name="todo",
    help="◆ A distinctive terminal todo manager",
    add_completion=False,
)

console = Console()
storage = TodoStorage()

# Nord-inspired palette (Minimalist Zen)
NORD_ACCENT = "#a3be8c"  # Soft green
NORD_PENDING = "#ebcb8b"  # Soft yellow
NORD_DONE = "#a3be8c"  # Soft green
NORD_BORDER = "#4c566a"  # Muted blue-gray


def header(title: str) -> None:
    """Display styled header with rounded borders."""
    rprint(
        Panel(
            f"[bold {NORD_ACCENT}]◆ {title}[/]",
            border_style=NORD_BORDER,
            padding=(0, 1),
        )
    )


def show_info(message: str) -> None:
    """Display info message with icon."""
    rprint(f"[{NORD_ACCENT}]▸[/] {message}")


def show_success(message: str) -> None:
    """Display success message with icon."""
    rprint(f"[{NORD_DONE}]✓[/] {message}")


def show_error(message: str) -> None:
    """Display error message with icon."""
    rprint(f"[bold red]✗[/] {message}")


def format_date(date_str: str) -> str:
    """Format ISO date to YYYY-MM-DD."""
    return datetime.fromisoformat(date_str).strftime("%Y-%m-%d")


@app.command()
def add(
    title: str = typer.Argument(..., help="Todo title"),
    description: Optional[str] = typer.Option(None, "--desc", "-d", help="Description"),
) -> None:
    """Add a new todo item."""
    header("ADD TODO")

    try:
        todo = Todo(title=title, description=description)
        created = storage.add(todo)

        show_info(f"Title: [bold]{created.title}[/]")
        if created.description:
            show_info(f"Desc: {created.description}")
        show_success(f"Created: [bold]{created.id}[/]")

    except ValueError as e:
        show_error(str(e))


@app.command(name="list")
def list_(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status (pending/done)"),
) -> None:
    """List all todos."""
    header("YOUR TODOS")

    # Get todos with optional filter
    if status:
        try:
            status_enum = Status(status)
            todos = storage.filter_by_status(status_enum)
        except ValueError:
            show_error(f"Invalid status: {status}")
            return
    else:
        todos = storage.list_all()

    if not todos:
        show_info("No todos found")
        return

    # Create styled table
    table = Table(
        title=None,
        border_style=NORD_BORDER,
        header_style=f"bold {NORD_ACCENT}",
        padding=(0, 1),
    )
    table.add_column("ID", style=NORD_PENDING)
    table.add_column("Title")
    table.add_column("Status", style=NORD_DONE)
    table.add_column("Date")

    for todo in todos:
        table.add_row(
            todo.id,
            todo.title,
            f"{todo.status_symbol} {todo.status}",
            format_date(todo.created_at),
        )

    console.print(table)
    show_info("Use [bold]todo complete <id>[/] to mark done")


@app.command()
def complete(id: str = typer.Argument(..., help="Todo ID")) -> None:
    """Mark a todo as complete."""
    header("COMPLETE TODO")

    todo = storage.get(id)
    if not todo:
        show_error(f"Todo not found: {id}")
        return

    if todo.status == Status.DONE:
        show_info(f"Already done: [bold]{id}[/]")
        return

    updated = storage.update(id, status=Status.DONE)
    if updated:
        show_success(f"Marked as done: [bold]{id}[/]")
    else:
        show_error(f"Failed to update: {id}")


@app.command()
def delete(id: str = typer.Argument(..., help="Todo ID")) -> None:
    """Delete a todo item."""
    header("DELETE TODO")

    if storage.delete(id):
        show_success(f"Deleted: [bold]{id}[/]")
    else:
        show_error(f"Todo not found: {id}")


if __name__ == "__main__":
    app()
