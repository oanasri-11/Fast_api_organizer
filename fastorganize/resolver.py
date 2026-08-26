from pathlib import Path
def build_module_map(
  project_root:Path,
  files:list[Path],
  root_package:str



):
 module_map={}
 for file in files :
  relative=file.relative_to(project_root)

  parts=list(relative.with_suffix(""),parts)

  if parts[-1]=="__init__":
   parts=parts[:1]
  module_name=".".join(parts) 
  module_map[module_name]=file


  return module_map

def resolve_import(
  import_name:str,module_map:dict[str,Path]
):
 if import_name in module_map:
  return module_map[import_name]  
 

 return None
