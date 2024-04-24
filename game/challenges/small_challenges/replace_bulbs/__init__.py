def get_savings_on_bulbs(number_of_rooms: int) -> str:
    price_of_1kwh = 1  # PLN
    power_of_oldtype_bulb = 60  # W
    power_of_led = 9  # W
    time_of_lighting = 365 * 4  # assumption that a bulb is used for 4 hours per each day
    cost_old_type_bulb = int(power_of_oldtype_bulb * 0.001 * time_of_lighting * price_of_1kwh)
    cost_led = int(power_of_led * 0.001 * time_of_lighting * price_of_1kwh)
    cost_for_household_oldtype_bulb = number_of_rooms*cost_old_type_bulb
    cost_for_household_led = number_of_rooms*cost_led
    return "Assuming that the bulb is used every day for a year for 4 hours, " \
        f"an old-type bulb consumes approximately {cost_old_type_bulb} zlotys, " \
        f"while an LED with the corresponding power consumes {cost_led} zlotys each year. " \
        f"When we take into account the number of rooms in your house ({number_of_rooms}) " \
        "and assume that all light bulbs are on for 4 hours every day for a year, " \
        f"this gives the amounts {cost_for_household_oldtype_bulb} PLN and {cost_for_household_led} PLN, " \
        f"respectively. You can save even {cost_for_household_oldtype_bulb-cost_for_household_led} zlotys per year."


def get_task_description_bulbs(number_of_rooms: int) -> str:
    """
    Returns a task description.
    """
    with open(
        "game/challenges/small_challenges/replace_bulbs/task_description.txt", "r", encoding="utf-8"
    ) as file:
        raw_text = file.read()
    complete_task = (
        raw_text + "\n" + get_savings_on_bulbs(number_of_rooms))
    return complete_task
