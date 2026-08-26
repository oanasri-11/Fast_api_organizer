import ast
from pathlib import Path
from dataclasses import dataclass
@dataclass
class FileAnalysis:
  path:str
  imports:list[str]
  functions:list[str]
  classes:list[str]

  
def analyze_file(file_path):
  code=file_path.read_text()
  tree=ast.parse(code)
  functions=[]
  imports=[]
  classes=[]
  for node in ast.walk(tree):
    if isinstance(node,ast.FunctionDef):
      functions.append(node.name)
    elif isinstance(node,ast.ClassDef):
      classes.append(node)
    elif isinstance(node,ast.ImportFrom):
      imports.append(node.module)
    elif isinstance(node,ast.Import):
      imports.append(node.names[0].name)  



  return {
  'imports:',imports,
  'functions:',functions,
  'classes:',classes,

  }     
  



  
