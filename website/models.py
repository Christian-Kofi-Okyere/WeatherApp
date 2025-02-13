"""
Module models: Contains data classes for weather description.
"""


# pylint: disable=too-many-instance-attributes


from dataclasses import dataclass


@dataclass
class WeatherDescriptionString:
    """Dataclass to store weather description string information."""
    coordinate: dict = None
    latitude: float = None
    longitude: float = None
    description: str = None
    main: str = None
    country: str = None
    name: str = None
    image: str = None


@dataclass
class WeatherDescriptionNumeric:
    """Dataclass to store numeric weather information."""
    temperature: float = None
    feels: float = None
    temp_min: float = None
    temp_max: float = None
    pressure: int = None
    humidity: int = None
    visibility: int = None
    wind: float = None
    code: int = None
