from flask import Blueprint, render_template
from flask import request
import requests
import os
from .models import Weather_Description_String, Weather_Description_Numeric

# Create a blueprint
main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/', methods=['GET', 'POST'])
@main_blueprint.route('/index', methods=['GET', 'POST'])
def index():
    weather_data_string = Weather_Description_String()
    weather_data_numeric = Weather_Description_Numeric()
    error_message = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        
        if city and country:
            api_key = os.getenv('WEATHER_KEY')  # I saved my key in .env file
            # print(api_key)  # This will print the key in the console or None
            url = (f"https://api.openweathermap.org/data/2.5/weather?"
            f"q={city},{state},{country}&appid={api_key}&units=metric")
            
            response = requests.get(url)

            if response.status_code == 200:

                # String Data
                data = response.json()
                weather_data_string.coordinate = data['coord']
                weather_data_string.description = data['weather'][0]['description']
                icon = data['weather'][0]['icon']
                weather_data_string.image = f"https://openweathermap.org/img/wn/{icon}@2x.png"
                weather_data_string.main = data['weather'][0]['main']
                weather_data_string.name = data['name']
                weather_data_string.country = data['sys']['country']

                # Numeric Data
                weather_data_numeric.temp_max = data['main']['temp_max']
                weather_data_numeric.temp_min = data['main']['temp_min']
                weather_data_numeric.feels = data['main']['feels_like']
                weather_data_numeric.pressure = data['main']['pressure']
                weather_data_numeric.humidity = data['main']['humidity']
                weather_data_numeric.visibility = data['visibility']
                weather_data_numeric.temperature = data['main']['temp']
                weather_data_numeric.code = data['cod']
                weather_data_numeric.wind = data['wind']['speed']

                
            else:
                error_message = "Unable to fetch weather data. Please check your inputs."
        else:
            error_message = "City and Country are required."
    
    return render_template('dashboard.html', weather_data_string = weather_data_string, 
                           weather_data_numeric = weather_data_numeric, error_message=error_message)