#Find Files && Folders 
from pathlib import Path

def scan_project(project_path:str):
  project=Path(project_path)
  py_files=list(project.rglob("*.py"))
  return py_files
