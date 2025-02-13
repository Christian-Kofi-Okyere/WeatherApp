"""
Module views: Contains Flask routes for the weather website.
"""

import os
import datetime


from flask import Blueprint, render_template, jsonify, url_for, request, session
import requests
from pytz import timezone


from .models import WeatherDescriptionString, WeatherDescriptionNumeric


# Create a blueprint
main_blueprint = Blueprint("main", __name__)


def get_weather_data(city, country, weather_data_string, weather_data_numeric):
    api_key = os.getenv("WEATHER_KEY")  # I saved my key in .env file

    location_query = f"{city},{country}"
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={location_query}&appid={api_key}&units=metric"
    )

    response = requests.get(url, timeout=5)

    if response.status_code == 200:
        data = response.json()

        # Populate string Data
        coord = data.get("coord", {})
        weather_data_string.coordinate = coord
        weather_data_string.latitude = coord.get("lat")
        weather_data_string.longitude = coord.get("lon")
        weather_data_string.description = data["weather"][0]["description"]
        icon = data["weather"][0]["icon"]
        weather_data_string.image = (
            f"https://openweathermap.org/img/wn/{icon}@2x.png"
        )
        weather_data_string.main = data["weather"][0]["main"]
        weather_data_string.name = data["name"]
        weather_data_string.country = data["sys"].get("country")

        # Numeric Data
        main_data = data.get("main", {})
        weather_data_numeric.temp_max = main_data.get("temp_max")
        weather_data_numeric.temp_min = main_data.get("temp_min")
        weather_data_numeric.feels = main_data.get("feels_like")
        weather_data_numeric.pressure = main_data.get("pressure")
        weather_data_numeric.humidity = main_data.get("humidity")
        weather_data_numeric.visibility = data.get("visibility")
        weather_data_numeric.temperature = main_data.get("temp")
        weather_data_numeric.code = data.get("cod")
        weather_data_numeric.wind = data.get("wind", {}).get("speed")

        return data
    else:
        error_message = "Unable to fetch weather data. Please check your inputs."


@main_blueprint.route("/", methods=["GET", "POST"])
@main_blueprint.route("/index", methods=["GET", "POST"])
def index():
    """Render the main index page with weather data."""
    weather_data_string = WeatherDescriptionString()
    weather_data_numeric = WeatherDescriptionNumeric()
    error_message = None
    time = datetime.datetime.now(timezone("US/Eastern")).strftime("%H:%M:%S")

    if request.method == "POST":
        # Attempt to get geolocation coordinates from the form
        city = request.form.get("city")
        _state = request.form.get("state")  # Renamed to _state because it is unused.
        country = request.form.get("country")
    else:
        city = session.get("name")
        country = session.get("country")

    get_weather_data(city, country, weather_data_string, weather_data_numeric)

    return render_template(
        "index.html",
        weather_data_string=weather_data_string,
        weather_data_numeric=weather_data_numeric,
        error_message=error_message,
        time=time,
    )


@main_blueprint.route("/save_location", methods=["GET", "POST"])
def save_location():
    """Save the user's geolocation and redirect to the index page."""
    data = request.json
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    api_key = os.getenv("WEATHER_KEY")
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={latitude}&lon={longitude}&appid={api_key}"
    )

    api_response = requests.get(url, timeout=5)
    if api_response.status_code == 200:
        data = api_response.json()
        session["name"] = data["name"]
        session["country"] = data["sys"]["country"]
    return jsonify({"redirect": url_for("main.index")})
