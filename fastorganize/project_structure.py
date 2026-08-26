from pathlib import Path
import ast 
def find_app_directory(project_root:Path):
  possible_dirs=["app","src"]
  for dir_name in possible_dirs:
    app_dir=project_root/dir_name
    if app_dir.is_dir():
      return app_dir

  raise FileNotFoundError("Could not find 'app' or 'src' directory in the project root.")  
def contains_fastapi_app(file_path: Path) -> bool:
    try:
        code = file_path.read_text(
            encoding="utf-8"
        )

        tree = ast.parse(code)

    except (SyntaxError, UnicodeDecodeError):
        return False

    for node in ast.walk(tree):

        if isinstance(node, ast.Assign):

            if not isinstance(node.value, ast.Call):
                continue

            call = node.value

            if not isinstance(call.func, ast.Name):
                continue

            if call.func.id != "FastAPI":
                continue

            return True

    return False