from .planner import MovePlan


def print_plan(plan: list[MovePlan]):

    if not plan:
        print("\nNo changes needed.")
        return

    print("\n")
    print("=" * 60)
    print("FastOrganize Plan")
    print("=" * 60)

    for index, move in enumerate(plan, start=1):

        print(f"\n[{index}] {move.reason}")

        print(f"FROM:")
        print(f"  {move.source}")

        print(f"TO:")
        print(f"  {move.destination}")

        print(f"Conflict: {move.conflict}")

        if move.affected_files:

            print("Affected files:")

            for file in move.affected_files:
                print(f"  - {file}")

        else:
            print("Affected files: none")

    print("\n" + "=" * 60)
    print(f"Total planned moves: {len(plan)}")
    print("=" * 60)    