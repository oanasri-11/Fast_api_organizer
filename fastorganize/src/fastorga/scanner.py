#Find Files && Folders 
from pathlib import Path
p=Path('C:/Users/HP/Desktop/Siraj')
files=p.rglob('*.py*')
for f in files:
  print(f)