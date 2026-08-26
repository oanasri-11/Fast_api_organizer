from fastorganize.project import analyze_project
from fastorganize.reporter import print_report
project_path = "C:/Users/HP/Desktop/Siraj/backend/app/routes"
results = analyze_project(project_path)
print_report(results)