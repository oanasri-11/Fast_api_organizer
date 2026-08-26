import ast
from pathlib import Path


def module_name_from_path(
    file_path: Path,
    project_root: Path
) -> str:

    relative = file_path.relative_to(project_root)

    parts = list(relative.with_suffix("").parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]

    return ".".join(parts)


def resolve_relative_import(
    file_path: Path,
    project_root: Path,
    node: ast.ImportFrom
) -> str | None:

    current_module = module_name_from_path(
        file_path,
        project_root
    )

    current_parts = current_module.split(".")

    # Remove current file name
    package_parts = current_parts[:-1]

    # Python's level:
    # .  -> level 1
    # .. -> level 2
    # ... -> level 3

    if node.level > len(package_parts):
        return None

    base_parts = package_parts[
        :len(package_parts) - node.level + 1
    ]

    if node.module:
        base_parts.append(node.module)

    return ".".join(base_parts)


def rewrite_imports(
    file_path: Path,
    project_root: Path,
    old_module: str,
    new_module: str
):

    code = file_path.read_text(
        encoding="utf-8"
    )

    tree = ast.parse(code)

    for node in ast.walk(tree):

        # -------------------------
        # from x import y
        # -------------------------

        if isinstance(node, ast.ImportFrom):

            # Absolute import
            if node.level == 0:

                if node.module == old_module:
                    node.module = new_module

            # Relative import
            else:

                resolved = resolve_relative_import(
                    file_path,
                    project_root,
                    node
                )

                if resolved == old_module:
                    node.level = 0
                    node.module = new_module

        # -------------------------
        # import x
        # -------------------------

        elif isinstance(node, ast.Import):

            for alias in node.names:

                if alias.name == old_module:
                    alias.name = new_module

    return ast.unparse(tree)