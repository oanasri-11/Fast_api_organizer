from .analyzer import FileAnalysis


def classify_file(file: FileAnalysis) -> str:
    """
    Determine the role of a Python file.

    Priority:
    1. AST-based detection
    2. Import-based detection
    3. Directory/name-based detection
    4. unknown
    """

    # --------------------------------
    # 1. AST detection
    # --------------------------------

    if file.file_type != "unknown":
        return file.file_type

    # --------------------------------
    # 2. Import-based detection
    # --------------------------------

    for import_name in file.imports:

        if import_name.startswith("sqlalchemy"):
            return "database"

        if import_name.startswith("pydantic"):
            return "schema"

        if import_name.startswith("fastapi"):
            return "route"

    # --------------------------------
    # 3. Path-based detection
    # --------------------------------

    path = file.path.lower().replace("\\", "/")

    # schemas
    if "/schemas/" in path or "/schema/" in path:
        return "schema"

    # models
    if "/models/" in path or "/model/" in path:
        return "model"

    # routes
    if "/routes/" in path or "/route/" in path:
        return "route"

    # services
    if "/services/" in path or "/service/" in path:
        return "service"

    # database
    if "/database/" in path or "/db/" in path:
        return "database"

    # configuration
    if (
        "/config/" in path
        or "/settings/" in path
        or "config.py" in path
        or "settings.py" in path
    ):
        return "config"

    # utilities
    if "/utils/" in path or "/utility/" in path:
        return "utility"

    # --------------------------------
    # 4. Filename-based detection
    # --------------------------------

    filename = path.split("/")[-1]

    if "service" in filename:
        return "service"

    if "schema" in filename:
        return "schema"

    if "model" in filename:
        return "model"

    if "route" in filename or "router" in filename:
        return "route"

    if "database" in filename:
        return "database"

    if "config" in filename or "settings" in filename:
        return "config"

    if "util" in filename:
        return "utility"

    # --------------------------------
    # 5. Unknown
    # --------------------------------

    return "unknown"