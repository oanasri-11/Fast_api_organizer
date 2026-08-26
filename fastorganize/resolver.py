from pathlib import Path


def build_module_map(
    project_root: Path,
    files: list[Path],
    root_package: str
):
    module_map = {}

    for file in files:
        relative = file.relative_to(project_root)
        parts = list(relative.with_suffix("").parts)

        if parts[-1] == "__init__":
            parts = parts[:-1]

        module_name = ".".join(parts)

        # Keep module names as discovered from project root.
        # root_package is currently detected upstream and reserved for future refinement.
        if root_package:
            if module_name.startswith(root_package):
                pass

        module_map[module_name] = file

    return module_map


def resolve_import(
    import_name: str,
    module_map: dict[str, Path]
):
    if not import_name:
        return None

    # Try the full import first, then progressively shorter package paths.
    # Example: app.models.users.schemas -> app.models.users -> app.models -> app
    parts = import_name.split(".")
    candidates = [import_name]

    for index in range(len(parts) - 1, 0, -1):
        candidates.append(".".join(parts[:index]))

    for candidate in candidates:
        target = module_map.get(candidate)
        if target is not None:
            return target

    return None
