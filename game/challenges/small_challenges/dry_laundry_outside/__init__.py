import requests
from secret import WEATHER_API_KEY


def _check_weather(city: str) -> str:
    """
    Returns a string with information if the current weather conditions are OK to
    dry user's washing ourside. It uses a city name to get this info.
    """
    base_url: str = "http://api.weatherapi.com/v1/current.json?"
    complete_url: str = f"{base_url}key={WEATHER_API_KEY}&q={city}"
    response = requests.get(complete_url)
    response_json = response.json()
    if "error" not in response_json:
        wind = response_json["current"]["wind_kph"]
        humidity = response_json["current"]["humidity"]
        temperature = response_json["current"]["temp_c"]
        if humidity > 60:
            return (
                f"The weather conditions aren't good to dry your washing, it's too wet ({humidity}%). "
                "Try to do this task another day! 😉"
            )
        elif wind > 30:
            return (
                "The weather conditions aren't good to dry your washing, it's too windy. "
                "Try to do this task another day! 😉"
            )
        elif temperature < 10:
            return (
                "The weather conditions aren't good to dry your washing, it's too cold. "
                "Try to do this task another day! 😉"
            )
        else:
            return "The weather conditions are great to dry your washing today 💚."
    else:
        return "You have to check the weather conditions on your own because there is a problem with app."


def get_task_description_laundry(users_city: str) -> str:
    """
    Returns a task description with information on weather conditions.
    """
    with open(
        "game/challenges/small_challenges/dry_laundry_outside/task_description.txt", "r", encoding="utf-8"
    ) as file:
        raw_text = file.read()
    complete_task = (
        raw_text + "\nDaily weather check ⛅💦💨:\n" + _check_weather(users_city)
    )
    return complete_task
