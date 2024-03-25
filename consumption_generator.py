import psycopg2
import json
import numpy as np
import random
import datetime
from typing import List, Optional, Dict, Tuple

class ConsumptionGenerator:
    def __init__(self, reading_date: datetime.datetime) -> None:
        self.db_connection: Optional[psycopg2.extensions.connection] 
        self.db_cursor: Optional[psycopg2.extensions.cursor] 
        self.db_connection, self.db_cursor = self._open_connection_with_db()
        if self.db_connection and self.db_cursor:
            self.generate_readings(reading_date)
        self._close_connection_with_db()

    def _open_connection_with_db(self) -> Tuple[Optional[psycopg2.extensions.cursor], 
                                                Optional[psycopg2.extensions.cursor]]:
        """
        Opens a connection with PostgreSQL database.
        """
        try:
            with open("appconfig.json", "r") as file:
                json_data: Dict = json.load(file)
            db_connection: psycopg2.extensions.connection = psycopg2.connect(**json_data)
            db_cursor: psycopg2.extensions.cursor = db_connection.cursor()
            print("PostgreSQL connection is opened")
            return db_connection, db_cursor
        except (Exception) as error:
            print("Failed to connect to database,", error)
            return None, None
        
    def _close_connection_with_db(self) -> None:
        """
        Closes a connection with PostgreSQL database.
        """
        if self.db_connection: 
            self.db_cursor.close()
            self.db_connection.close()
            print("PostgreSQL connection is closed")

    def generate_energy_consumption(self, hour_of_reading: int) -> float:
        """
        Function generating energy consumption for a given hour (in kW).
        """
        amplitude: float = 0.3
        period: int = 24  
        offset: float = 0.3  
        energy_usage: float = amplitude * np.sin(2 * np.pi * hour_of_reading / period) + offset
        return energy_usage

    def generate_noise(self) -> float:
        """
        Introduces noise into the electricity consumption profile for a given household.
        """
        return random.uniform(-0.2, 0.2)    

    def get_all_meters(self) -> List[int]:
        """
        Gets all ID's to generate readings for them. 
        """
        query: str = "SELECT id_meter FROM meter"
        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_the_latest_reading(self) -> int:
        """
        Gets the biggest ID from the Reading table.
        If there is no readings, it returns 0 and the first reading will have ID equals 1.
        """
        query: str = "SELECT MAX(id_reading) FROM reading;"
        self.db_cursor.execute(query)
        fetched: Optional[int] = self.db_cursor.fetchone()[0]
        return fetched if fetched else 0  

    def add_reading_to_table(self, id_reading: int, time: str, used_energy: float, meter_id_meter: int) -> None:
        """
        Adds reading to the Reading table.
        """
        try: 
            query: str = f"INSERT INTO reading(id_reading, time, used_energy, meter_id_meter) VALUES ({id_reading}, '{str(time)}', {used_energy}, {meter_id_meter});"
            self.db_cursor.execute(query)
            print("Record inserted successfully into the Reading table")
        except (Exception) as error:
            print("Failed to insert record into the Reading table,", error)

    def generate_readings(self, reading_date: datetime.datetime) -> None:
        """
        Generates reading for each meter in db. Commits transaction at the end.
        """
        all_meters: List[int] = self.get_all_meters()
        last_reading_id: int = self.get_the_latest_reading()
        for meter in all_meters:
            last_reading_id += 1
            self.add_reading_to_table(
                last_reading_id, 
                reading_date,
                max(0, (self.generate_energy_consumption(reading_date.hour) + self.generate_noise())),
                meter[0]
                )
        self.db_connection.commit()

dt: datetime = datetime.datetime(2020, 2, 12)
tm: datetime = datetime.time(1, 0)
combined_date: datetime = dt.combine(dt, tm)
timestamp: datetime = datetime.datetime.now()
consumption_generator: ConsumptionGenerator = ConsumptionGenerator(combined_date)
