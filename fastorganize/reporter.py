from .planner import MovePlan

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




def print_plan(plan: list[MovePlan]):

    if not plan:
        print("No changes needed.")
        return

    print()
    print("FastOrganize Plan")
    print("=" * 50)

    for move in plan:

        print()
        print(f"FROM: {move.source}")
        print(f"TO:   {move.destination}")
        print(f"WHY:  {move.reason}")

        if move.affected_files:
            print("AFFECTED FILES:")

            for file in move.affected_files:
                print(f"  - {file}")

        if move.conflict:
            print("⚠ CONFLICT: destination already exists")

        else:
            print("✓ SAFE")

    print()
    print("=" * 50)      