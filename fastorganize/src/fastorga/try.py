from pathlib import Path
import ast

file = Path("C:/Users/HP/Desktop/Siraj/backend/app/routes/users.py")

code = file.read_text()

tree = ast.parse(code)
#Finding functions :

"""

for node in ast.walk(tree):
    if isinstance(node,ast.FunctionDef):
        print(node.name)


"""

#findig imports :
"""

for node in ast.walk(tree):
  if isinstance(node,ast.Import):
    for name in node.names:
      print(name.name)
  elif isinstance(node,ast.ImportFrom):
    print(node.module)
    """
#finding classes:
"""

for node in ast.walk(tree):
  if isinstance(node,ast.ClassDef):
    print(node.name)
     """



#find routes
for node in ast.walk(tree):
  if isinstance(node,ast.FunctionDef):
    for decorator in node.decorator_list:
      print(ast.dump(decorator,indent=2))
