
from dataclasses import dataclass

@dataclass
class Weather_Description_String():
    
    coordinate: dict = None
    description: str = None
    main: str = None
    country: str = None
    name: str = None
    image: str = None

@dataclass
class Weather_Description_Numeric():

    temperature: float = None
    feels: float = None
    temp_min: float = None
    temp_max: float = None
    pressure: int = None
    humidity: int = None
    visibility: int = None
    wind: float = None
    code: int = None
