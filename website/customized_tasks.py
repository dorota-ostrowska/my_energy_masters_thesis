import requests
from website.models import Address
from website.secret import WEATHER_API_KEY

from website.configuration_guide import MAC, WINDOWS


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
                f"The weather conditions in {city} aren't good to dry your washing, it's too wet ({humidity}%). "
                "Try to do this task another day! 😉"
            )
        elif wind > 30:
            return (
                f"The weather conditions in {city} aren't good to dry your washing, it's too windy ({wind} kmph). "
                "Try to do this task another day! 😉"
            )
        elif temperature < 10:
            return (
                f"The weather conditions in {city} aren't good to dry your washing, it's too cold ({temperature}℃). "
                "Try to do this task another day! 😉"
            )
        else:
            return (
                f"The weather conditions in {city} are great to dry your washing today 💚. "
                f"\n💧 humidity: {humidity}% 💦 wind: {wind} kmph 💨 temperature: {temperature}℃ 🌡️"
            )
    else:
        return f"You have to check the weather conditions in {city} on your own because there is a problem with app."


def get_task_dry_laundry_outside(description_template: str, user: str) -> str:
    """
    Returns a task description with information on weather conditions in user's location.
    """
    address = (
        Address.query.filter_by(id_address=user.id_clients_mailing_address)
        .with_entities(Address.city)
        .first()
    )
    return description_template.format(weather_today=(_check_weather(address[0])))


def _get_savings_on_bulbs(number_of_rooms: int) -> dict:
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
    subtract = cost_for_household_oldtype_bulb - cost_for_household_led
    return {
        "cost_old_type_bulb": cost_old_type_bulb,
        "cost_led": cost_led,
        "number_of_rooms": number_of_rooms,
        "cost_for_household_oldtype_bulb": cost_for_household_oldtype_bulb,
        "cost_for_household_led": cost_for_household_led,
        "subtract": subtract,
    }


def get_task_replace_bulbs(description_template: str, user: str) -> str:
    """
    Returns a task description.
    It takes a customized string for user with calculated savings on bulbs too.
    """
    return description_template.format(**_get_savings_on_bulbs(user.number_of_rooms))


def get_task_sleep_mode(description_template: str, user: str) -> str:
    """
    Returns a task description.
    """
    return description_template.format(
        link_guide=f"How to configure it? 🧐🤔 Windows 🖥️: {WINDOWS} MAC 🍎: {MAC}"
    )
