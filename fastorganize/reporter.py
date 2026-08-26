def print_report(results):
  print("FastOrganize Report")
  for result in results:
    print(f"\nFile: {result.path}")

    print("Imports:")
    for imp in result.imports:
      print(f"  - {imp}")
    print("Functions:")
    for func in result.functions:
      print(f"  - {func}")
    print("Classes:")
    for cls in result.classes:
      print(f"  - {cls}")