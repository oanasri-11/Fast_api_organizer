from fastorga.scanner import scan_project

files=scan_project("C:/Users/HP/Desktop/Fast_api_organizer/fastorganize/src/fastorga")
for file in files:
  print(file)

