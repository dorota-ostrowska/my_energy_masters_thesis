<div align="center">
  <br>
  <h1>MyEnergy 💡🐷💸</h1>
  <strong>Act locally, think globally: save energy!</strong>
</div>
<br>
<p align="center">
    <img src="website/static/images/readme/made_with.svg">
    <img src="website/static/images/readme/built_with.svg">
    <img src="website/static/images/readme/to_save.svg">
</p>

Welcome to my repository housing the code for my master's thesis in Computer Science at PJAIT (Warsaw, Poland). This platform presents an excellent opportunity for me to hone my Fullstack skills while aspiring to make a positive impact on our planet. 🌱

## What is MyEnergy? 🌱

We are MyEnergy, more than just an electricity seller. Our mission is to empower you to **create a better world for yourself and future generations**. Did you know that the past decade is likely to have been the hottest period in the last 125,000 years?
🌞 The production of electricity has a huge impact on our environment. This environmental fact underscores the urgency of our mission. By adopting sustainable habits like acting locally and thinking globally, we can mitigate these effects. We're here to assist you in your daily energy-saving efforts. Let's make a difference together – **YOU and MyEnergy**! 💡

## Table of contents 📖

- [What is MyEnergy? 🌱](#what-is-myenergy-)
- [Table of contents 📖](#table-of-contents-)
- [Technologies 🛠](#technologies-)
- [Getting started 🎬](#getting-started-)
  - [Run locally 🏠](#run-locally-)

## Technologies 🛠

- **Python 3.12**: The primary programming language used for application logic.
  
- **Flask**: A lightweight web framework used for building MyEnergy web application.
  
- **PostgreSQL**: A relational database used for storing application data.

- **SQLAlchemy**: An ORM (Object-Relational Mapping) tool for managing the database using Python objects.

- More technologies and their versions are listed in the **requirements.txt** file.

## Getting started 🎬

### Run locally 🏠

1. Open Docker Desktop application.

2. Go to a main folder of project.

   ```bash
   cd masters_thesis_s27951
   ```

3. Run a script in terminal.

   ```bash
   ./run_postgresql.sh
   ```

4. Create tables in the database and add init data to them.
   Run scripts from database_myenergy folder.

5. Create your own appconfig.json using as na example appconfig_example.json file.

6. Create a `secret.py` file in `website` folder with your own two secrets: `WEATHER_API_KEY` from `https://www.weatherapi.com/` (generate it for free) and `FLASK_KEY = "super-key"` (hardcoded).

7. Create a virtual environment.

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

8. Install necessary requirements.

   ```bash
   pip install -r requirements.txt
   ```

9. Create meter readings in db (add appropriate dates).

10. Run `app.py` file.

   ```bash
   python consumption_generator.py
   ```
   
[⬆ Back to top](#table-of-contents)
