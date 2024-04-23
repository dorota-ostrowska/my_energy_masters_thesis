from configuration_guide import WINDOWS, MAC
def get_task_description_sleep_mode() -> str:
    """
    Returns a task description.
    """
    with open(
        "game/challenges/small_challenges/set_sleep_mode/task_description.txt", "r", encoding="utf-8"
    ) as file:
        raw_text = file.read()
    complete_task = f"{raw_text}\nWindows🟦: {WINDOWS}\nMAC🍎: {MAC}"
    return complete_task
