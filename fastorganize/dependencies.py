from pathlib import Path

from .analyzer import FileAnalysis
from .resolver import resolve_import


def build_dependency_graph(
    results: list[FileAnalysis],
    module_map: dict[str, Path]
):
    graph = {}

    for result in results:

        file_path = Path(result.path)

        dependencies = []

        for import_name in result.imports:

            target = resolve_import(
                import_name,
                module_map
            )

            if target is not None:
                dependencies.append(target)

        graph[file_path] = dependencies

    return graph