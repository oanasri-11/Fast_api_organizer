import ast
from pathlib import Path


def path_to_module(
    file_path: Path,
    project_root: Path
) -> str:

    relative = file_path.relative_to(project_root)

    parts = list(
        relative.with_suffix("").parts
    )

    if parts[-1] == "__init__":
        parts = parts[:-1]

    return ".".join(parts)


def rewrite_imports(
    file_path: Path,
    old_module: str,
    new_module: str
) -> str:

    code = file_path.read_text(
        encoding="utf-8"
    )

    tree = ast.parse(code)

    lines = code.splitlines()

    for node in ast.walk(tree):

        # -------------------------
        # import app.users
        # -------------------------

        if isinstance(node, ast.Import):

            for alias in node.names:

                if alias.name == old_module:

                    line = lines[node.lineno - 1]

                    lines[node.lineno - 1] = line.replace(
                        alias.name,
                        new_module,
                        1
                    )

        # -------------------------
        # from app.users import User
        # -------------------------

        elif isinstance(node, ast.ImportFrom):

            if node.module == old_module:

                line = lines[node.lineno - 1]

                lines[node.lineno - 1] = line.replace(
                    old_module,
                    new_module,
                    1
                )

    return "\n".join(lines)
def prepare_import_changes(
    move_plan,
    project_root: Path
):
    old_module = path_to_module(
        move_plan.source,
        project_root
    )

    new_module = path_to_module(
        move_plan.destination,
        project_root
    )

    changes = []

    for affected_file in move_plan.affected_files:

        new_code = rewrite_imports(
            affected_file,
            old_module,
            new_module
        )

        changes.append(
            {
                "file": affected_file,
                "old_module": old_module,
                "new_module": new_module,
                "new_code": new_code
            }
        )

    return changes