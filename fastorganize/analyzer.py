import ast
from dataclasses import dataclass


@dataclass
class RouteInfo:
    method: str
    path: str
    function: str


@dataclass
class FileAnalysis:
    """
    Represents the analysis of a single Python file.
    """

    path: str
    imports: list[str]
    functions: list[str]
    classes: list[str]
    routes: list[RouteInfo]
    file_type: str


def is_pydantic_model(node):
    if not isinstance(node, ast.ClassDef):
        return False

    for base in node.bases:
        if isinstance(base, ast.Name):
            if base.id == "BaseModel":
                return True

    return False


def is_sqlalchemy_model(node):
    if not isinstance(node, ast.ClassDef):
        return False

    for base in node.bases:
        if isinstance(base, ast.Name):
            if base.id == "Base":
                return True

    return False


def extract_route(decorator, function_name):
    if not isinstance(decorator, ast.Call):
        return None

    if not isinstance(decorator.func, ast.Attribute):
        return None

    if not isinstance(decorator.func.value, ast.Name):
        return None

    # Only detect @app.get(), @app.post(), etc.
    if decorator.func.value.id != "app":
        return None

    method = decorator.func.attr.upper()

    if not decorator.args:
        return None

    path_node = decorator.args[0]

    if not isinstance(path_node, ast.Constant):
        return None

    path = path_node.value

    if not isinstance(path, str):
        return None

    return RouteInfo(
        method=method,
        path=path,
        function=function_name
    )


def analyze_file(file_path):

    try:
        code = file_path.read_text(
            encoding="utf-8"
        )

        tree = ast.parse(code)

    except (SyntaxError, UnicodeDecodeError) as error:

        print(
            f"Error parsing {file_path}: {error}"
        )

        return None

    functions = []
    imports = []
    classes = []
    routes = []

    has_route = False
    has_model = False
    has_schema = False

    for node in ast.walk(tree):

        # -------------------------
        # Functions + FastAPI routes
        # -------------------------

        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef)
        ):

            functions.append(node.name)

            for decorator in node.decorator_list:

                route = extract_route(
                    decorator,
                    node.name
                )

                if route:
                    routes.append(route)
                    has_route = True

        # -------------------------
        # Classes
        # -------------------------

        elif isinstance(node, ast.ClassDef):

            classes.append(node.name)

            if is_pydantic_model(node):
                has_schema = True

            if is_sqlalchemy_model(node):
                has_model = True

        # -------------------------
        # from x import y
        # -------------------------

        elif isinstance(node, ast.ImportFrom):

            if node.module:
                imports.append(node.module)

        # -------------------------
        # import x
        # -------------------------

        elif isinstance(node, ast.Import):

            for name in node.names:
                imports.append(name.name)

    # -------------------------
    # Determine file type
    # -------------------------

    if has_route:
        file_type = "route"

    elif has_schema:
        file_type = "schema"

    elif has_model:
        file_type = "model"

    else:
        file_type = "unknown"

    # -------------------------
    # Return analysis
    # -------------------------

    return FileAnalysis(
        path=str(file_path),
        imports=imports,
        functions=functions,
        classes=classes,
        routes=routes,
        file_type=file_type
    )