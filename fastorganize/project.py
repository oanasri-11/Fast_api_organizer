from fastorganize.scanner import scan_project
from fastorganize.analyzer import analyze_file
from pathlib import Path
import ast 


def analyze_project(project_path):
   files=scan_project(project_path)
   results=[]
   for file in files:
      result=analyze_file(file)
      results.append(result)