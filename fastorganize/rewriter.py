import ast
from pathlib import Path

def module_name_from_path(
    file_path:Path,
    project_root:Path,

)->str:
  relative=file_path.relative(project_root)
  parts = list(relative.with_suffix("").parts)

  if parts[-1] == "__init__":
        parts = parts[:-1]

  return ".".join(parts)


def rewrite_imports(
    file_path: Path,
    old_module: str,
    new_module: str
):

    code = file_path.read_text(encoding="utf-8")

    tree = ast.parse(code)

    for node in ast.walk(tree):

        if isinstance(node, ast.ImportFrom):

            if node.module == old_module:

                node.module = new_module

    return ast.unparse(tree)
