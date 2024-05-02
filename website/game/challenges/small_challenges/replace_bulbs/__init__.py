def get_savings_on_bulbs(number_of_rooms: int) -> str:
    """
    Returns a customized string for user with calculated savings on bulbs.
    Calculates savings using a following folmula:
    K[PLN] = P[W] * 0.001 * t[h] * pkwh[PLN/kWh],
    where:
    K - cost of energy consumed by a light source
    P - power of a light source
    t - light source operating time
    pkwh - price of 1 kWh of electricity.
    This function calculates savings taking into account the number of rooms.
    It's personalized.
    """
    price_of_1kwh: int = 1  # PLN
    power_of_oldtype_bulb: int = 60  # W
    power_of_led: int = 9  # W
    time_of_lighting: int = (
        365 * 4
    )  # assumption that a bulb is used for 4 hours per each day
    cost_old_type_bulb: int = int(
        power_of_oldtype_bulb * 0.001 * time_of_lighting * price_of_1kwh
    )
    cost_led: int = int(power_of_led * 0.001 * time_of_lighting * price_of_1kwh)
    cost_for_household_oldtype_bulb: int = number_of_rooms * cost_old_type_bulb
    cost_for_household_led: int = number_of_rooms * cost_led
    return (
        "Assuming that the bulb is used every day for a year for 4 hours, "
        f"an old-type bulb consumes approximately {cost_old_type_bulb} zlotys, "
        f"while an LED with the corresponding power consumes {cost_led} zlotys each year. "
        f"When we take into account the number of rooms in your house ({number_of_rooms}) "
        "and assume that there is one regular bulb per room "
        "and all light bulbs are on for 4 hours every day for a year, "
        f"this gives the amounts {cost_for_household_oldtype_bulb} PLN and {cost_for_household_led} PLN, "
        "for old-type bulbs and LEDs respectively. You can save even "
        f"{cost_for_household_oldtype_bulb-cost_for_household_led} zlotys per year."
    )


def get_task_description_bulbs(number_of_rooms: int) -> str:
    """
    Returns a task description.
    It takes a customized string for user with calculated savings on bulbs too.
    """
    with open(
        "game/challenges/small_challenges/replace_bulbs/task_description.txt",
        "r",
        encoding="utf-8",
    ) as file:
        raw_text = file.read()
    complete_task = raw_text + "\n" + get_savings_on_bulbs(number_of_rooms)
    return complete_task
