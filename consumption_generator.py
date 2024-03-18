import psycopg2
import json
import numpy as np
import matplotlib.pyplot as plt
import random
import datetime

def generate_energy_consumption(hour: int) -> float:
    """
    Function generating energy consumption for a given hour (in kW).
    """
    amplitude = 0.3
    period = 24  
    offset = 1.7  
    energy_usage = amplitude * np.sin(2 * np.pi * hour / period) + offset
    return max(0, energy_usage)

def add_noise() -> float:
    """
    Introduces noise into the electricity consumption profile for a given household.
    """
    return random.uniform(-0.2, 0.2)

def get_meter_ids(cursor):
    query = "SELECT id_meter FROM meter"
    cursor.execute(query)
    return cursor.fetchall()

def get_the_biggest_id_from_id_reading():
    query = "SELECT MAX(id_reading) FROM reading;"
    cursor.execute(query)
    fetched = cursor.fetchall()[0][0]
    biggest_reading = fetched if fetched else 0
    return biggest_reading

def add_reading(id_reading: int, time: str, used_energy: float, meter_id_meter: int):
    print(id_reading, time, used_energy, meter_id_meter)
    try: 
        query = f"INSERT INTO reading(id_reading, time, used_energy, meter_id_meter) VALUES ({id_reading}, '{time}', {used_energy}, {meter_id_meter});"
        cursor.execute(query)
        conn.commit()
        print("Record inserted successfully into reading table")
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into reading table", error)

with open("appconfig.json", "r") as file:
    json_data = json.load(file)
conn = psycopg2.connect(**json_data)
cursor = conn.cursor()
all_meters = get_meter_ids(cursor)
biggest_id = get_the_biggest_id_from_id_reading()
current_timestamp = datetime.datetime.now()
for meter in all_meters:
    biggest_id += 1
    add_reading(
        biggest_id, 
        str(current_timestamp),
        (generate_energy_consumption(current_timestamp.hour)+add_noise()), 
        meter[0]
        )
if conn:
    cursor.close()
    conn.close()
    print("PostgreSQL connection is closed")
