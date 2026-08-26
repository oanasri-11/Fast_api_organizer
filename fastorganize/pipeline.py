from pathlib import Path

from .scanner import scan_project
from .analyzer import analyze_file
from .resolver import build_module_map
from .dependencies import build_dependency_graph
from .reverse import build_reverse_dependencies
from .planner import create_plan
from .reporter import print_plan
from .project_structure import find_app_directory


def analyze_project(project_root: Path):

    print("Scanning project...")

    files = scan_project(project_root)

    print(f"Found {len(files)} Python files.")

    # -------------------------
    # Analyze files
    # -------------------------

    results = []

    for file in files:

        result = analyze_file(file)
        if result is not None :

         results.append(result)

    print("Analysis complete.")
    print("\nDetected files:")







    for result in results:
     print(f"{result.path} -> {result.file_type}")
        
    

    # -------------------------
    # Find application directory
    # -------------------------

    app_directory = find_app_directory(
        project_root
    )

    print(f"Application directory: {app_directory}")

    # -------------------------
    # Build module map
    # -------------------------

    module_map = build_module_map(
        project_root,
        files,
        app_directory.name
    )

    # -------------------------
    # Dependency graph
    # -------------------------

    dependency_graph = build_dependency_graph(
        results,
        module_map
    )

    # -------------------------
    # Reverse dependencies
    # -------------------------

    reverse_dependencies = build_reverse_dependencies(
        dependency_graph
    )

    # -------------------------
    # Create organization plan
    # -------------------------

    plan = create_plan(
        results,
        app_directory,
        reverse_dependencies
    )

    # -------------------------
    # Show plan
    # -------------------------

    print_plan(plan)

    return plan