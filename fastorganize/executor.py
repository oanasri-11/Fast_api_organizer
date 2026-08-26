from .planner import MovePlan


def execute_plan(
    plan: list[MovePlan],
    dry_run: bool = True
):

    for move in plan:

        if move.conflict:
            print(
                f"SKIPPING: {move.source}"
                f" → {move.destination}"
            )
            print("Reason: destination already exists")
            print()
            continue

        print(f"MOVE:")
        print(f"  FROM: {move.source}")
        print(f"  TO:   {move.destination}")
        print(f"  WHY:  {move.reason}")
        print()

        if dry_run:
            continue

        move.destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        move.source.rename(
            move.destination
        )