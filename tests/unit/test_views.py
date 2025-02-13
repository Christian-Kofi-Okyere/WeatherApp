import os
import pytest
from website.views import get_weather_data
from website.models import WeatherDescriptionString, WeatherDescriptionNumeric

# Define a DummyResponse class to simulate requests.Response
class DummyResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json_data = json_data

    def json(self):
        return self._json_data

def dummy_success_response(*args, **kwargs):
    data = {
        "coord": {"lon": 0.0, "lat": 0.0},
        "weather": [{
            "description": "rainy",
            "icon": "09d",
            "main": "Rain"
        }],
        "name": "SuccessCity",
        "sys": {"country": "SC"},
        "main": {
            "temp": 15.0,
            "feels_like": 14.0,
            "temp_min": 13.0,
            "temp_max": 17.0,
            "pressure": 1012,
            "humidity": 50
        },
        "visibility": 10000,
        "wind": {"speed": 3.0},
        "cod": 200
    }
    return DummyResponse(200, data)

def dummy_failure_response(*args, **kwargs):
    return DummyResponse(404, {})

def test_get_weather_data_success(mocker):
    os.environ["WEATHER_KEY"] = "dummy_key"
    weather_str = WeatherDescriptionString()
    weather_num = WeatherDescriptionNumeric()
    # Patch requests.get to return our dummy success response.
    mocker.patch("website.views.requests.get", dummy_success_response)
    data = get_weather_data("TestCity", "TC", weather_str, weather_num)
    assert data is not None
    assert weather_str.name == "SuccessCity"
    assert weather_str.description == "rainy"
    assert weather_num.temperature == 15.0
    assert weather_num.pressure == 1012

def test_get_weather_data_failure(mocker):
    os.environ["WEATHER_KEY"] = "dummy_key"
    weather_str = WeatherDescriptionString()
    weather_num = WeatherDescriptionNumeric()
    # Patch requests.get to simulate a failure.
    mocker.patch("website.views.requests.get", dummy_failure_response)
    data = get_weather_data("TestCity", "TC", weather_str, weather_num)
    # On failure, our function returns None and leaves the objects unpopulated.
    assert data is None
    assert weather_str.name is None
    assert weather_num.temperature is None
