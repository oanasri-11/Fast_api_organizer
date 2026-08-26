from pathlib import Path


def scan_project(project_path):
  project=Path(project_path)
  python_files=list(project.rglob("*.py"))
  return python_files 