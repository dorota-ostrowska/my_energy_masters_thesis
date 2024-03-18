import psycopg2
import json
import numpy as np
import matplotlib.pyplot as plt
import random
import datetime
from typing import List, Optional, Dict

def generate_energy_consumption(hour: int) -> float:
    """
    Function generating energy consumption for a given hour (in kW).
    """
    amplitude: float = 0.3
    period: int = 24  
    offset: float = 0.3  
    energy_usage: float = amplitude * np.sin(2 * np.pi * hour / period) + offset
    return energy_usage

def add_noise() -> float:
    """
    Introduces noise into the electricity consumption profile for a given household.
    """
    return random.uniform(-0.2, 0.2)

def get_meter_ids(cursor) -> List[int]:
    query: str = "SELECT id_meter FROM meter"
    cursor.execute(query)
    return cursor.fetchall()

def get_the_biggest_id_from_id_reading() -> int:
    """
    Gets the biggest ID from the Reading table.
    If there is no readings, it returns 0 and the first reading will have ID equals 1.
    """
    query: str = "SELECT MAX(id_reading) FROM reading;"
    cursor.execute(query)
    fetched: Optional[int] = cursor.fetchone()[0]
    return fetched if fetched else 0  

def add_reading(id_reading: int, time: str, used_energy: float, meter_id_meter: int) -> None:
    """
    Adds reading to the Reading table.
    """
    try: 
        query: str = f"INSERT INTO reading(id_reading, time, used_energy, meter_id_meter) VALUES ({id_reading}, '{time}', {used_energy}, {meter_id_meter});"
        cursor.execute(query)
        conn.commit()
        print("Record inserted successfully into the Reading table")
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the Reading table", error)

def show_consumption_profile() -> None:
    hours = np.arange(24)
    energy_consumption = [max(0, ((generate_energy_consumption(hour) + add_noise()) for hour in hours))]
    plt.plot(hours, energy_consumption, marker='o')
    plt.title('Energy consumption for a household (example)')
    plt.xlabel('hour')
    plt.ylabel('used power [kW]')
    plt.grid(True)
    plt.xticks(np.arange(0, 24, step=1))
    plt.show()

try:
    with open("appconfig.json", "r") as file:  # open a connection
        json_data: Dict = json.load(file)
    conn: psycopg2.extensions.connection = psycopg2.connect(**json_data)
    cursor: psycopg2.extensions.cursor = conn.cursor()
    print("PostgreSQL connection is opened")
except (Exception, psycopg2.Error) as error:
    print("Failed to connect to database", error)
all_meters: List[int] = get_meter_ids(cursor)
biggest_id: int = get_the_biggest_id_from_id_reading()
current_timestamp: datetime = datetime.datetime.now()
for meter in all_meters:
    biggest_id += 1
    add_reading(
        biggest_id, 
        str(current_timestamp),
        max(0, (generate_energy_consumption(current_timestamp.hour) + add_noise())),
        meter[0]
        )
if conn:  # close a connection
    cursor.close()
    conn.close()
    print("PostgreSQL connection is closed")

# show_consumption_profile()
