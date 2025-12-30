"""CLI commands for todo app using typer and rich for beautiful output."""
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from todo_cli.models import TodoStatus
from todo_cli.storage import TodoStorage
from todo_cli.tui import run_tui

app = typer.Typer(help="╔═══════════════════════════════════════╗\n║      ✦ CLI Todo App ✦               ║\n╚═══════════════════════════════════════╝")
console = Console()


def get_storage() -> TodoStorage:
    """Get storage instance."""
    return TodoStorage()


@app.command()
def add(
    title: str = typer.Argument(..., help="Todo title"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Todo description"),
):
    """Add a new todo.

    Examples:
        todo add "Buy groceries"
        todo add "Call mom" --description "Discuss birthday plans"
    """
    storage = get_storage()
    todo = storage.create(title, description)

    console.print(f"\n✨ [bold green]Todo created:[/bold green]")
    console.print(f"   [dim]ID:[/dim] {todo.id}")
    console.print(f"   [dim]Title:[/dim] {todo.title}")
    if todo.description:
        console.print(f"   [dim]Description:[/dim] {todo.description}")


@app.command()
def list(
    status: Optional[TodoStatus] = typer.Option(None, "--status", "-s", help="Filter by status"),
):
    """List all todos.

    Examples:
        todo list
        todo list --status pending
        todo list -s done
    """
    storage = get_storage()
    todos = storage.get_all(status=status)

    if not todos:
        console.print("\n[dim]╶ No todos found. Use 'todo add' to create one.[/dim]")
        return

    # Create beautiful table
    table = Table(title="\n✦ Your Todos", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Title", style="white")
    table.add_column("Status", style="yellow", width=10)
    table.add_column("Created", style="dim", width=20)

    for todo in todos:
        status_style = "green" if todo.status == TodoStatus.DONE else "yellow"
        table.add_row(
            str(todo.id),
            todo.title,
            f"[{status_style}]{todo.status.value}[/{status_style}]",
            todo.created_at[:10],
        )

    console.print("\n")
    console.print(table)


@app.command()
def complete(
    todo_id: int = typer.Argument(..., help="Todo ID to complete"),
):
    """Mark a todo as done.

    Examples:
        todo complete 1
    """
    storage = get_storage()
    todo = storage.get_by_id(todo_id)

    if not todo:
        console.print(f"\n[bold red]✗ Error:[/bold red] Todo with ID {todo_id} not found")
        raise typer.Exit(1)

    if todo.status == TodoStatus.DONE:
        console.print(f"\n[dim]◉ Todo {todo_id} is already done[/dim]")
        return

    storage.update(todo_id, status=TodoStatus.DONE)
    console.print(f"\n[bold green]✓ Todo {todo_id} marked as done![/bold green]")


@app.command()
def delete(
    todo_id: int = typer.Argument(..., help="Todo ID to delete"),
):
    """Delete a todo.

    Examples:
        todo delete 1
    """
    storage = get_storage()
    todo = storage.get_by_id(todo_id)

    if not todo:
        console.print(f"\n[bold red]✗ Error:[/bold red] Todo with ID {todo_id} not found")
        raise typer.Exit(1)

    if not storage.delete(todo_id):
        console.print(f"\n[bold red]✗ Error:[/bold red] Failed to delete todo {todo_id}")
        raise typer.Exit(1)

    console.print(f"\n[bold red]✗ Todo {todo_id} deleted[/bold red]")


@app.command()
def tui():
    """Launch interactive terminal UI.

    Examples:
        todo tui
    """
    console.print("\n[bold yellow]Launching Terminal UI...[/bold yellow]")
    console.print("[dim]Press 'q' to exit[/dim]\n")
    run_tui()


if __name__ == "__main__":
    app()
