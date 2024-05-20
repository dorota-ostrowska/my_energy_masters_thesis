"""
This module contains functions that customize the content of challenges for users based
on their location, household details, and current weather conditions. The primary goal
is to provide personalized task descriptions that are relevant and useful for the users.

Functions:
    _check_weather(city: str) -> str:
        Check the current weather conditions for drying laundry outside.
        
    get_task_dry_laundry_outside(description_template: str, user: str) -> str:
        Generate a task description for drying laundry outside with weather information.
        
    _get_savings_on_bulbs(number_of_rooms: int) -> dict:
        Calculate potential savings from replacing old-type bulbs with LED bulbs.
        
    get_task_replace_bulbs(description_template: str, user: str) -> str:
        Generate a task description for replacing bulbs with calculated savings.
        
    get_task_sleep_mode(description_template: str, user: str) -> str:
        Generate a task description for configuring sleep mode on devices.
"""

import requests
from website.models import Address
from website.secret import WEATHER_API_KEY

from website.configuration_guide import MAC, WINDOWS


def _check_weather(city: str) -> str:
    """
    Check the current weather conditions for drying laundry outside.

    This function fetches the current weather data for a specified city using the
    WeatherAPI. It checks the wind speed, humidity, and temperature to determine
    if the conditions are suitable for drying laundry outside.

    Args:
        city (str): The name of the city to check the weather for.

    Returns:
        str: A message indicating whether the weather conditions are suitable
             for drying laundry outside. The message includes the humidity, wind speed,
             and temperature. If the weather conditions are not suitable, the message
             provides the reason why.
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
    Generate a task description for drying laundry outside with weather information.

    This function fetches the user's city from the database, checks the current
    weather conditions for that city, and returns a task description that includes
    weather information.

    Args:
        description_template (str): The template for the task description.
        user (str): The user object containing user details.

    Returns:
        str: A formatted task description with weather information.
    """
    address = (
        Address.query.filter_by(id_address=user.id_clients_mailing_address)
        .with_entities(Address.city)
        .first()
    )[0]
    return description_template.format(weather_today=(_check_weather(address)))


def _get_savings_on_bulbs(number_of_rooms: int) -> dict:
    """
    Calculate potential savings from replacing old-type bulbs with LED bulbs.

    This function calculates the annual energy cost savings for a household
    when replacing old-type (incandescent) bulbs with LED bulbs. The savings
    are calculated based on the number of rooms in the household.

    Args:
        number_of_rooms (int): The number of rooms in the user's household.

    Returns:
        dict: A dictionary containing the cost details for old-type bulbs, LED bulbs,
              and the savings for the household.
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
    Generate a task description for replacing bulbs with calculated savings.

    This function calculates the potential savings from replacing old-type bulbs
    with LED bulbs based on the number of rooms in the user's household. It returns
    a task description that includes these savings.

    Args:
        description_template (str): The template for the task description.
        user (str): The user object containing user details, including the number of rooms.

    Returns:
        str: A formatted task description with savings information.
    """
    return description_template.format(**_get_savings_on_bulbs(user.number_of_rooms))


def get_task_sleep_mode(description_template: str, user: str) -> str:
    """
    Generate a task description for configuring sleep mode on devices.

    This function returns a task description that includes links to guides
    for configuring sleep mode on Windows and MAC devices.

    Args:
        description_template (str): The template for the task description.
        user (str): The user object.

    Returns:
        str: A formatted task description with links to sleep mode configuration guides.
    """
    return description_template.format(
        link_guide=f"How to configure it? 🧐🤔 Windows 🖥️: {WINDOWS} MAC 🍎: {MAC}"
    )
