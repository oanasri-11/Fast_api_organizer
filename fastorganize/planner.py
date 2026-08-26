from dataclasses import dataclass
from pathlib import Path

from .analyzer import FileAnalysis
from .classifier import classify_file


@dataclass
class MovePlan:
    source: Path
    destination: Path
    reason: str


def create_plan(
    results: list[FileAnalysis],
    project_root: Path
):
    plan = []

    for file in results:

        file_type = classify_file(file)

        source = Path(file.path)

        if file_type == "route":
            destination = project_root / "app" / "routes" / source.name

        elif file_type == "schema":
            destination = project_root / "app" / "schemas" / source.name

        elif file_type == "model":
            destination = project_root / "app" / "models" / source.name

        elif file_type == "service":
            destination = project_root / "app" / "services" / source.name

        elif file_type == "database":
            destination = project_root / "app" / "database" / source.name

        elif file_type == "config":
            destination = project_root / "app" / "config" / source.name

        elif file_type == "utility":
            destination = project_root / "app" / "utils" / source.name

        else:
            continue

        if source != destination:
            plan.append(
                MovePlan(
                    source=source,
                    destination=destination,
                    reason=f"Detected as {file_type}"
                )
            )

    return plan