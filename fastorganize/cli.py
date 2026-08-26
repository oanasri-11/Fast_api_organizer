from pathlib import Path

import typer

from .pipeline import analyze_project


app = typer.Typer(
    help="FastOrganize - FastAPI project organizer"
)


@app.command()
def analyze(
    project: Path = typer.Argument(
        ...,
        help="Path to the FastAPI project"
    )
):
    """Analyze a FastAPI project."""

    if not project.exists():
        typer.echo(f"Project does not exist: {project}")
        raise typer.Exit(code=1)

    if not project.is_dir():
        typer.echo(f"Not a directory: {project}")
        raise typer.Exit(code=1)

    analyze_project(project)


if __name__ == "__main__":
    app(prog_name="fastorganize")