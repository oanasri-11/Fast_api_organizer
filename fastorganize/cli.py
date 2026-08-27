from pathlib import Path

import typer

from .pipeline import analyze_project
from .executor import execute_plan


app = typer.Typer(
    help="FastOrganize - FastAPI project organizer"
)


@app.command()
def version():
    typer.echo("FastOrganize version 1.0.0")

@app.command()
def analyze(
    project: str
):
    """
    Analyze a FastAPI project and show
    the organization plan.

    This command NEVER modifies files.
    """

    project_path = Path(project)

    if not project_path.exists():
        typer.echo(
            f"Project does not exist: {project}"
        )
        raise typer.Exit(code=1)

    if not project_path.is_dir():
        typer.echo(
            f"Not a directory: {project}"
        )
        raise typer.Exit(code=1)

    typer.echo("Analyzing project...")

    plan = analyze_project(
        project_path
    )

    if not plan:
        typer.echo(
            "No changes needed."
        )
        return

    typer.echo("")
    typer.echo(
        f"Found {len(plan)} planned changes."
    )

    for index, move in enumerate(
        plan,
        start=1
    ):

        typer.echo("")
        typer.echo(
            f"[{index}] {move.reason}"
        )

        typer.echo(
            f"  FROM: {move.source}"
        )

        typer.echo(
            f"  TO:   {move.destination}"
        )

        if move.conflict:

            typer.echo(
                "  WARNING: destination exists"
            )


@app.command()
def apply(
    project: str
):
    """
    Apply the organization plan.

    The project is backed up before
    any modification is made.
    """

    project_path = Path(project)

    if not project_path.exists():
        typer.echo(
            f"Project does not exist: {project}"
        )
        raise typer.Exit(code=1)

    if not project_path.is_dir():
        typer.echo(
            f"Not a directory: {project}"
        )
        raise typer.Exit(code=1)

    typer.echo(
        "Analyzing project..."
    )

    plan = analyze_project(
        project_path
    )

    if not plan:

        typer.echo(
            "No changes needed."
        )

        return

    typer.echo("")
    typer.echo(
        f"Found {len(plan)} planned changes."
    )

    typer.echo("")
    typer.echo(
        "The following changes will be applied:"
    )

    for index, move in enumerate(
        plan,
        start=1
    ):

        typer.echo(
            f"\n[{index}] {move.reason}"
        )

        typer.echo(
            f"  FROM: {move.source}"
        )

        typer.echo(
            f"  TO:   {move.destination}"
        )

        if move.conflict:

            typer.echo(
                "  WARNING: destination exists"
            )

    typer.echo("")

    confirmed = typer.confirm(
        "Do you want to apply these changes?"
    )

    if not confirmed:

        typer.echo(
            "Operation cancelled."
        )

        return

    typer.echo("")
    typer.echo(
        "Applying changes..."
    )

    success = execute_plan(
        plan,
        project_path,
        dry_run=False
    )

    if success:

        typer.echo("")
        typer.echo(
            "FastOrganize completed successfully."
        )

    else:

        typer.echo("")
        typer.echo(
            "FastOrganize failed. "
            "Changes were rolled back."
        )

        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()