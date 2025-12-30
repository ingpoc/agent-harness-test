"""CLI Todo App - Main entry point with distinctive terminal design.

Aesthetic: Minimalist Zen
- Palette: Nord-inspired cool blues on dark gray
- Borders: Rounded (╭─╮│╰╯)
- Status symbols: ▸ pending, ✓ done, ○ empty
"""

from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(
    name="todo",
    help="◆ A distinctive terminal todo manager",
    add_completion=False,
)

console = Console()

# Nord-inspired palette (Minimalist Zen)
NORD = {
    "bg": "#2e3440",
    "fg": "#eceff4",
    "accent": "#a3be8c",  # Soft green
    "pending": "#ebcb8b",  # Soft yellow
    "done": "#a3be8c",  # Soft green
    "border": "#4c566a",  # Muted blue-gray
}


def header(title: str) -> None:
    """Display styled header with rounded borders."""
    rprint(
        Panel(
            f"[bold {NORD['accent'}]◆ {title}[/]",
            border_style=NORD["border"],
            padding=(0, 1),
        )
    )


def show_info(message: str) -> None:
    """Display info message with icon."""
    rprint(f"[{NORD['accent']}]▸[/] {message}")


def show_success(message: str) -> None:
    """Display success message with icon."""
    rprint(f"[{NORD['done']}]✓[/] {message}")


def show_error(message: str) -> None:
    """Display error message with icon."""
    rprint(f"[bold red]✗[/] {message}")


@app.command()
def add(
    title: str = typer.Argument(..., help="Todo title"),
    description: Optional[str] = typer.Option(None, "--desc", "-d", help="Description"),
) -> None:
    """Add a new todo item."""
    header("ADD TODO")
    show_info(f"Adding: [bold]{title}[/]")
    if description:
        show_info(f"Desc: {description}")
    show_success("Todo created!")
    # TODO: Implement actual storage


@app.command()
def list_(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
) -> None:
    """List all todos."""
    header("YOUR TODOS")

    # Create styled table
    table = Table(
        title=None,
        border_style=NORD["border"],
        header_style=f"bold {NORD['accent']}",
        padding=(0, 1),
    )
    table.add_column("ID", style=NORD["pending"])
    table.add_column("Title")
    table.add_column("Status", style=NORD["done"])
    table.add_column("Date")

    # Demo data - replace with actual todos
    table.add_row("F-001", "Add authentication", "▸ pending", "2025-12-30")
    table.add_row("F-002", "Setup database", "✓ done", "2025-12-30")
    table.add_row("F-003", "Write tests", "○ empty", "2025-12-30")

    console.print(table)

    show_info("Use [bold]todo complete <id>[/] to mark done")


@app.command()
def complete(id: str = typer.Argument(..., help="Todo ID")) -> None:
    """Mark a todo as complete."""
    header("COMPLETE TODO")
    show_info(f"Marking as done: [bold]{id}[/]")
    show_success("Todo completed!")
    # TODO: Implement actual completion


@app.command()
def delete(id: str = typer.Argument(..., help="Todo ID")) -> None:
    """Delete a todo item."""
    header("DELETE TODO")
    show_info(f"Deleting: [bold]{id}[/]")
    show_success("Todo deleted!")
    # TODO: Implement actual deletion


if __name__ == "__main__":
    app()
