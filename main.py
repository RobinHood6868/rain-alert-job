import requests
import os
from dotenv import load_dotenv
import smtplib


# 1. Load values from .env
load_dotenv()

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")


# 2. Weather data for Hanoi, Viet Nam
LAT = 21.027763
LONG = 105.834160

parameters = {
    "lat": LAT,
    "lon": LONG,
    "appid": WEATHER_API_KEY,
    "cnt": 6
}


# 3. Main execution
API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
response = requests.get(API_ENDPOINT, params=parameters)
response.raise_for_status()
hours_data = response.json()["list"]

will_rain = False
for data in hours_data:
    condition_code = data["weather"][0]["id"]
    if condition_code < 700:
        will_rain = True

if will_rain:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="minhdung0056@gmail.com",
            msg="Subject: Rain Alert\n\n"
                "Please bring your umbrella today!"
        )