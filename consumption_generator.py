import psycopg2
import psycopg2.extras
import json
import numpy as np
import random
import datetime


class ConsumptionGenerator:
    def __init__(self) -> None:
        self.db_connection: psycopg2.extensions.connection | None
        self.db_cursor: psycopg2.extensions.cursor | None
        self.db_connection, self.db_cursor = self._open_connection_with_db()

    def _open_connection_with_db(
        self,
    ) -> tuple[
        psycopg2.extensions.cursor | None, psycopg2.extensions.cursor | None
    ]:
        """
        Opens a connection with PostgreSQL database.
        """
        try:
            with open("appconfig.json", "r") as file:
                json_data: dict = json.load(file)
            db_connection: psycopg2.extensions.connection = psycopg2.connect(
                **json_data
            )
            db_cursor: psycopg2.extensions.cursor = db_connection.cursor()
            print("PostgreSQL connection is opened")
            return db_connection, db_cursor
        except Exception as error:
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
        energy_usage: float = (
            amplitude * np.sin(2 * np.pi * hour_of_reading / period) + offset
        )
        return energy_usage

    def generate_noise(self) -> float:
        """
        Introduces noise into the electricity consumption profile for a given household.
        """
        return random.uniform(-0.2, 0.2)

    def get_all_meters(self) -> list[int]:
        """
        Gets all ID's to generate readings for them.
        """
        query: str = "SELECT id_meter FROM meter"
        self.db_cursor.execute(query)
        return [row[0] for row in self.db_cursor.fetchall()]

    def add_readings_to_table(
        self, readings: list[tuple[int, str, float, int]]
    ) -> None:
        """
        Adds multiple readings to the Reading table.

        This method inserts a batch of energy consumption readings into the Reading table.
        It uses the `psycopg2.extras.execute_values` method to efficiently insert multiple rows in a single query.

        Parameters:
        readings (list of tuples): A list of tuples where each tuple represents a reading.
                                   Each tuple contains the following elements:
                                   - id_reading (int): The unique identifier for the reading.
                                   - time (str): The timestamp of the reading.
                                   - used_energy (float): The amount of energy used (in kW).
                                   - id_meter (int): The identifier of the meter for which the reading was taken.

        The method performs the following steps:
        1. Constructs an SQL query for inserting multiple readings.
        2. Uses `psycopg2.extras.execute_values` to execute the query and insert the readings.
        3. Prints a success message indicating the number of records inserted.
        
        In case of an error during the insertion process, it catches the exception and prints an error message.

        Example usage:
            readings = [
                (1, '2024-05-18 12:00:00', 0.35, 101),
                (2, '2024-05-18 12:15:00', 0.40, 102),
                ...
            ]
            self.add_readings_to_table(readings)
        """
        try:
            query: str = """INSERT INTO reading (time, used_energy, id_meter) 
                            VALUES %s"""
            psycopg2.extras.execute_values(self.db_cursor, query, readings)
            print(f"{len(readings)} records inserted successfully into the reading table")
        except Exception as error:
            print("Failed to insert records into the reading table,", error)

    def generate_readings(self, start_date: datetime.datetime, end_date: datetime.datetime, interval_minutes: int = 15) -> None:
        """
        Generates readings for each meter in the database over a specified date range with the given interval.

        This method generates simulated energy consumption readings for all meters in the database.
        The readings are generated at intervals specified by `interval_minutes` from `start_date` to `end_date`.
        The generated readings are then inserted into the database in a single transaction.

        Parameters:
        start_date (datetime): The starting date and time for generating readings.
        end_date (datetime): The ending date and time for generating readings.
        interval_minutes (int, optional): The interval between readings in minutes. Default is 15 minutes.

        The method performs the following steps:
        1. Fetches all meter IDs from the database.
        2. Fetches the latest reading ID from the database to ensure unique reading IDs.
        3. Iterates over the specified date range, generating readings for each meter at each interval.
        4. Accumulates the generated readings in a list.
        5. Inserts all accumulated readings into the database in a single transaction.
        """
        all_meters: list[int] = self.get_all_meters()
        current_date: datetime.datetime = start_date

        readings = []

        while current_date <= end_date:
            for meter in all_meters:
                reading = (
                    current_date,
                    max(
                        0,
                        (
                            self.generate_energy_consumption(current_date.hour)
                            + self.generate_noise()
                        ),
                    ),
                    meter,
                )
                readings.append(reading)

            current_date += datetime.timedelta(minutes=interval_minutes)

        self.add_readings_to_table(readings)
        self.db_connection.commit()


start_date: datetime.datetime = datetime.datetime(2024, 1, 1)
end_date: datetime.datetime = datetime.datetime(2024, 1, 2)

consumption_generator = ConsumptionGenerator()

consumption_generator.generate_readings(start_date, end_date)

consumption_generator._close_connection_with_db()
