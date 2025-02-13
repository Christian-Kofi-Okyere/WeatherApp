import pytest
from website.models import WeatherDescriptionString, WeatherDescriptionNumeric


def test_weather_description_string_defaults():
    """Test that the default values for WeatherDescriptionString are None."""
    wds = WeatherDescriptionString()
    assert wds.coordinate is None
    assert wds.latitude is None
    assert wds.longitude is None
    assert wds.description is None
    assert wds.main is None
    assert wds.country is None
    assert wds.name is None
    assert wds.image is None


def test_weather_description_string_custom_values():
    """Test setting custom values for WeatherDescriptionString."""
    coordinate = {"lat": 40.7128, "lon": -74.0060}
    wds = WeatherDescriptionString(
        coordinate=coordinate,
        latitude=40.7128,
        longitude=-74.0060,
        description="clear sky",
        main="Clear",
        country="US",
        name="New York",
        image= None
    )
    assert wds.coordinate == coordinate
    assert wds.latitude == 40.7128
    assert wds.longitude == -74.0060
    assert wds.description == "clear sky"
    assert wds.main == "Clear"
    assert wds.country == "US"
    assert wds.name == "New York"
    assert wds.image == None


def test_weather_description_numeric_defaults():
    """Test that the default values for WeatherDescriptionNumeric are None."""
    wdn = WeatherDescriptionNumeric()
    assert wdn.temperature is None
    assert wdn.feels is None
    assert wdn.temp_min is None
    assert wdn.temp_max is None
    assert wdn.pressure is None
    assert wdn.humidity is None
    assert wdn.visibility is None
    assert wdn.wind is None
    assert wdn.code is None


def test_weather_description_numeric_custom_values():
    """Test setting custom values for WeatherDescriptionNumeric."""
    wdn = WeatherDescriptionNumeric(
        temperature=25.0,
        feels=26.5,
        temp_min=22.0,
        temp_max=28.0,
        pressure=1013,
        humidity=60,
        visibility=10000,
        wind=5.5,
        code=200
    )
    assert wdn.temperature == 25.0
    assert wdn.feels == 26.5
    assert wdn.temp_min == 22.0
    assert wdn.temp_max == 28.0
    assert wdn.pressure == 1013
    assert wdn.humidity == 60
    assert wdn.visibility == 10000
    assert wdn.wind == 5.5
    assert wdn.code == 200
