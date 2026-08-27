from pathlib import Path
import shutil
import tempfile

from .planner import MovePlan
from .validator import (
    validate_python_files,
    validate_imports,
)
from .import_rewriter import prepare_import_changes


def create_backup(project_root: Path) -> Path:
    """Create a complete backup of the project."""

    backup_root = Path(
        tempfile.mkdtemp(prefix="fastorganize_")
    )

    backup_project = backup_root / project_root.name

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
    """Restore the project from a backup."""

    if project_root.exists():
        shutil.rmtree(project_root)

    shutil.copytree(
        backup_project,
        project_root
    )

    print("Project restored from backup.")


def execute_plan(
    plan: list[MovePlan],
    project_root: Path,
    dry_run: bool = True
) -> bool:
    """
    Execute a move plan safely.

    dry_run=True:
        Show what would happen without modifying files.

    dry_run=False:
        Backup, move, rewrite imports,
        validate, and rollback on failure.
    """

    if not plan:
        print("No changes to apply.")
        return True

    # ==================================================
    # DRY RUN
    # ==================================================

    if dry_run:

        for move in plan:

            print()
            print("=" * 60)
            print("MOVE")
            print("=" * 60)

            print(f"FROM: {move.source}")
            print(f"TO:   {move.destination}")
            print(f"Reason: {move.reason}")

            if move.conflict:
                print(
                    "WARNING: destination already exists."
                )
            else:
                print("Would move file.")

        print()
        print("=" * 60)
        print("DRY RUN COMPLETE")
        print("No files were modified.")
        print("=" * 60)

        return True

    # ==================================================
    # BACKUP
    # ==================================================

    backup_project = create_backup(
        project_root
    )

    try:

        # ==================================================
        # MOVE + IMPORT REWRITE
        # ==================================================

        for move in plan:

            print()
            print(
                f"Processing: {move.source}"
            )

            # ------------------------------------------
            # Conflict
            # ------------------------------------------

            if move.conflict:

                print(
                    f"Skipping conflict: "
                    f"{move.destination}"
                )

                continue

            # ------------------------------------------
            # Prepare import changes
            # ------------------------------------------

            changes = prepare_import_changes(
                move,
                project_root
            )

            # ------------------------------------------
            # Create destination directory
            # ------------------------------------------

            move.destination.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            # ------------------------------------------
            # Move file
            # ------------------------------------------

            shutil.move(
                str(move.source),
                str(move.destination)
            )

            print(
                f"Moved: {move.source}"
            )

            print(
                f"     -> {move.destination}"
            )

            # ------------------------------------------
            # Apply import changes
            # ------------------------------------------

            for change in changes:

                file = change["file"]
                new_code = change["new_code"]

                file.write_text(
                    new_code,
                    encoding="utf-8"
                )

                print(
                    f"Updated imports: {file}"
                )

        # ==================================================
        # SYNTAX VALIDATION
        # ==================================================

        print()
        print("=" * 60)
        print("VALIDATING PYTHON SYNTAX")
        print("=" * 60)

        valid, failed_files = (
            validate_python_files(
                project_root
            )
        )

        if not valid:

            print(
                "Syntax validation failed!"
            )

            for file in failed_files:

                print(
                    f"Invalid Python: {file}"
                )

            print()
            print(
                "Rolling back changes..."
            )

            restore_backup(
                project_root,
                backup_project
            )

            return False

        print(
            "Python syntax validation passed."
        )

        # ==================================================
        # IMPORT VALIDATION
        # ==================================================

        print()
        print("=" * 60)
        print("VALIDATING IMPORTS")
        print("=" * 60)

        imports_valid, failed_imports = (
            validate_imports(
                project_root
            )
        )

        if not imports_valid:

            print(
                "Import validation failed!"
            )

            for import_error in failed_imports:

                print(
                    f"Broken import: "
                    f"{import_error}"
                )

            print()
            print(
                "Rolling back changes..."
            )

            restore_backup(
                project_root,
                backup_project
            )

            return False

        print(
            "Import validation passed."
        )

        # ==================================================
        # SUCCESS
        # ==================================================

        print()
        print("=" * 60)
        print("EXECUTION SUCCESSFUL")
        print("=" * 60)

        print(
            "All changes were applied "
            "and validated successfully."
        )

        print(
            f"Backup available at: "
            f"{backup_project}"
        )

        return True

    # ==================================================
    # UNEXPECTED ERROR
    # ==================================================

    except Exception as error:

        print()
        print("=" * 60)
        print("EXECUTION FAILED")
        print("=" * 60)

        print(
            f"Error: {error}"
        )

        print()
        print(
            "Rolling back changes..."
        )

        try:

            restore_backup(
                project_root,
                backup_project
            )

        except Exception as rollback_error:

            print(
                "CRITICAL: Rollback failed!"
            )

            print(
                f"Rollback error: "
                f"{rollback_error}"
            )

            return False

        return False