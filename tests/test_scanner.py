from fastorganize.scanner import scan_project
project="C:/Users/HP/Desktop/Siraj/backend/app/models"
files=scan_project(project) 
for file in files:
  print(file )