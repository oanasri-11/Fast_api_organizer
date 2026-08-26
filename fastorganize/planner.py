from dataclasses import dataclass
from pathlib import Path

from .analyzer import FileAnalysis
from .classifier import classify_file


@dataclass
class MovePlan:

    source: Path
    destination: Path
    reason: str
    affected_files: list[Path]
    conflict: bool


def create_plan(
    results: list[FileAnalysis],
    app_directory: Path,
    reverse_dependencies: dict[Path, list[Path]]
):
    plan = []

    for file in results:

        file_type = classify_file(file)

        source = Path(file.path)

        destination = None

        if file_type == "route":
            destination = (
                app_directory
                / "routes"
                / source.name
            )

        elif file_type == "schema":
            destination = (
                app_directory
                / "schemas"
                / source.name
            )

        elif file_type == "model":
            destination = (
                app_directory
                / "models"
                / source.name
            )

        elif file_type == "service":
            destination = (
                app_directory
                / "services"
                / source.name
            )

        elif file_type == "database":
            destination = (
                app_directory
                / "database"
                / source.name
            )

        elif file_type == "config":
            destination = (
                app_directory
                / "config"
                / source.name
            )

        elif file_type == "utility":
            destination = (
                app_directory
                / "utils"
                / source.name
            )

        # Unknown files are not moved
        if destination is None:
            continue

        affected_files = reverse_dependencies.get(
            source,
            []
        )

        if source != destination:
            conflict=destination.exists()

            plan.append(
                MovePlan(
                    source=source,
                    destination=destination,
                    reason=f"Detected as {file_type}",
                    affected_files=affected_files,
                    conflict=conflict
                )
            )

    return plan