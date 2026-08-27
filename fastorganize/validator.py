import ast
from pathlib import Path


def validate_python_files(
    project_root: Path
) -> tuple[bool, list[Path]]:
    """Validate Python syntax in the project."""

    failed_files = []

    for file in project_root.rglob("*.py"):

        try:
            code = file.read_text(
                encoding="utf-8"
            )

            ast.parse(code)

        except (UnicodeDecodeError, SyntaxError):

            failed_files.append(file)

    return (
        len(failed_files) == 0,
        failed_files
    )


def validate_imports(
    project_root: Path
) -> tuple[bool, list[str]]:
    """
    Validate internal absolute and relative imports.
    """

    failed_imports = []

    for file in project_root.rglob("*.py"):

        try:
            code = file.read_text(
                encoding="utf-8"
            )

            tree = ast.parse(code)

        except (UnicodeDecodeError, SyntaxError):

            continue

        for node in ast.walk(tree):

            # ==================================
            # import app.models.user
            # ==================================

            if isinstance(node, ast.Import):

                for alias in node.names:

                    module = alias.name

                    if module.startswith("app."):

                        if not module_exists(
                            module,
                            project_root
                        ):

                            failed_imports.append(
                                f"{file}: {module}"
                            )

            # ==================================
            # from app.models import User
            # ==================================

            elif isinstance(
                node,
                ast.ImportFrom
            ):

                # Relative import
                if node.level > 0:

                    module_exists_result = (
                        relative_module_exists(
                            file,
                            node,
                            project_root
                        )
                    )

                    if not module_exists_result:

                        failed_imports.append(
                            f"{file}: "
                            f"relative import "
                            f"{node.module}"
                        )

                # Absolute import
                elif node.module:

                    module = node.module

                    if module.startswith("app."):

                        if not module_exists(
                            module,
                            project_root
                        ):

                            failed_imports.append(
                                f"{file}: {module}"
                            )

    return (
        len(failed_imports) == 0,
        failed_imports
    )


def module_exists(
    module: str,
    project_root: Path
) -> bool:
    """Check whether an absolute module exists."""

    parts = module.split(".")

    module_path = project_root.joinpath(
        *parts
    )

    file_path = module_path.with_suffix(
        ".py"
    )

    package_path = (
        module_path / "__init__.py"
    )

    return (
        file_path.exists()
        or package_path.exists()
    )


def relative_module_exists(
    current_file: Path,
    node: ast.ImportFrom,
    project_root: Path
) -> bool:
    """
    Resolve imports such as:

        from .users import User
        from ..models import User
    """

    # ----------------------------------
    # Find current package directory
    # ----------------------------------

    current_dir = current_file.parent

    # ----------------------------------
    # node.level:
    #
    # .   -> level 1
    # ..  -> level 2
    # ... -> level 3
    # ----------------------------------

    target_dir = current_dir

    for _ in range(node.level - 1):

        target_dir = target_dir.parent

    # ----------------------------------
    # Add imported module
    # ----------------------------------

    if node.module:

        parts = node.module.split(
            "."
        )

        target_path = target_dir.joinpath(
            *parts
        )

    else:

        target_path = target_dir

    # ----------------------------------
    # module.py
    # ----------------------------------

    file_path = target_path.with_suffix(
        ".py"
    )

    if file_path.exists():
        return True

    # ----------------------------------
    # module/__init__.py
    # ----------------------------------

    package_path = (
        target_path / "__init__.py"
    )

    if package_path.exists():
        return True

    return False