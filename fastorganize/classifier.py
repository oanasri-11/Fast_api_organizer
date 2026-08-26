from .analyzer import FileAnalysis
#Recuves fileanalysis(functions,import,....)  and returns a role ( route,schmea,service,.....)
def classify_file(file:FileAnalysis)->str:
  if file.file_type!="unknown":
    return file.file_type

  for import_name in file.imports:
    if import_name.startswith('sqlalchemy'):
      return 'database'

  path=file.path.lower()

  if "config" in path or "settings" in path:
    return 'config'

  if "service" in path or "services" in path:
    return 'service'
  

  if "util" in path or "utils" in path :
    return "utility"



  return "unknown"  