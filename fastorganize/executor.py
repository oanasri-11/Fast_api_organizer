from pathlib import Path
import shutil
import tempfile

from .planner import MovePlan


def create_backup(project_root: Path) -> Path:
    """
    Create a complete backup of the project.

    Returns the path to the backup directory.
    """

    backup_root = Path(
        tempfile.mkdtemp(
            prefix="fastorganize_"
        )
    )

    backup_project = (
        backup_root / project_root.name
    )

    shutil.copytree(
        project_root,
        backup_project
    )

    print(f"Backup created: {backup_project}")

    return backup_project


def restore_backup(
    project_root: Path,
    backup_project: Path
):
    """
    Restore the project from a backup.
    """

    if project_root.exists():
        shutil.rmtree(project_root)

    shutil.copytree(
        backup_project,
        project_root
    )

    print("Project restored from backup.")


def execute_plan(
    plan: list[MovePlan],
    dry_run: bool = True
):
    """
    Execute a list of file moves.

    dry_run=True:
        Do not modify anything.

    dry_run=False:
        Move files.
    """

    if not plan:
        print("No changes to apply.")
        return

    for move in plan:

        print()
        print("=" * 60)
        print("MOVE")
        print("=" * 60)

        print(f"FROM: {move.source}")
        print(f"TO:   {move.destination}")

        if move.conflict:

            print(
                "WARNING: Destination already exists."
            )

            if dry_run:
                print(
                    "Dry run: skipping this move."
                )
            else:
                print(
                    "Move skipped because of conflict."
                )

            continue

        if dry_run:

            print(
                "Dry run: no files changed."
            )

            continue

        move.destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.move(
            str(move.source),
            str(move.destination)
        )

        print("Move completed.")

    print()
    print("=" * 60)

    if dry_run:
        print("DRY RUN COMPLETE")
        print("No files were modified.")
    else:
        print("EXECUTION COMPLETE")

    print("=" * 60)