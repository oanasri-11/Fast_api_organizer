from pathlib import Path


def build_reverse_dependencies(
    graph: dict[Path, list[Path]]
) :
    reversed_graph = {}
    for file_path,dep in graph.items():
        for dependency in dep:
            if dependency not in reversed_graph:
                reversed_graph[dependency] = []
            reversed_graph[dependency].append(file_path)

    return reversed_graph