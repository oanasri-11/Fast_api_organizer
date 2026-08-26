from pathlib import Path
from .analyzer import FileAnalysis

def dep_graph(results:list[FileAnalysis]):
    graph = {}
    for result in results:
        file_path=Path(result.path)
        graph[str(file_path)] = result.imports
    return graph