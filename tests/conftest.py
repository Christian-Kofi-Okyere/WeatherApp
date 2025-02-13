import pytest
import os
import sys

# Add the parent directory to the system path so that the website package can be found.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from website import create_app

# Define a DummyResponse class to simulate requests.Response
class DummyResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json_data = json_data

    def json(self):
        return self._json_data

@pytest.fixture(scope='module')
def test_client():
    # Set the Testing configuration prior to creating the Flask application
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        yield test_client  # This is where the testing happens!

@pytest.fixture(scope='function')
def weather_api_mock_client(mocker):
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    
    # Define dummy data that mimics a successful API response
    dummy_data = {
        'coord': {'lon': -0.1276, 'lat': 51.5073},
        'weather': [{
            'id': 804,
            'main': 'Clouds',
            'description': 'overcast clouds',
            'icon': '04n'
        }],
        'name': 'London',
        'sys': {'country': 'GB'},
        'main': {
            'temp': 3.87,
            'feels_like': 1.5,
            'temp_min': 3.36,
            'temp_max': 4.46,
            'pressure': 1022,
            'humidity': 88
        },
        'visibility': 9000,
        'wind': {'speed': 2.57, 'deg': 340},
        'clouds': {'all': 100},
        'cod': 200
    }
    
    # Patch the requests.get call in the views module to return our dummy response.
    mocker.patch(
        "website.views.requests.get",
        return_value=DummyResponse(200, dummy_data)
    )
    
    flask_app = create_app()
    with flask_app.test_client() as test_client:
        yield test_client
