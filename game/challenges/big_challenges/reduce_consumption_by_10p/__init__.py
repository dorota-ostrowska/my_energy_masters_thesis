def get_and_compare_current_consumption(current_weekly_consumption: float) -> str:
    pkwh: float = 1  # PLN, cost of 1 kWh
    expected_annual_savings: int = int(current_weekly_consumption * 52 * 0.1 * pkwh)
    return (
        f"Currently, your average weekly electricity consumption is approximately {current_weekly_consumption} kWh. "
        f"If you reduced them by only 10% (it's easy - trust me), you could save approximately PLN {expected_annual_savings} per year."
    )


def get_task_description_reduce_consumption_by_10p(
    current_weekly_consumption: float,
) -> str:
    """
    Returns a task description.
    """
    with open(
        "game/challenges/big_challenges/reduce_consumption_by_10p/task_description.txt",
        "r",
        encoding="utf-8",
    ) as file:
        raw_text = file.read()
    # implement in GUI a choice of systems (MAC or Windows) to display a guide
    complete_task = f"{raw_text}\n{get_and_compare_current_consumption(current_weekly_consumption)} 🥳"
    return complete_task
