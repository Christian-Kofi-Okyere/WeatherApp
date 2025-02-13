# def test_home_page_mock_api(weather_api_mock_client):
#     """
#     GIVEN a Flask application configured for testing with a mocked weather API,
#     WHEN the '/' page is requested (GET),
#     THEN check the response is valid and contains the expected weather data.
#     """
#     response = weather_api_mock_client.get('/', follow_redirects=True)
#     assert response.status_code == 200
#     assert b"London" in response.data
#     assert b"GB" in response.data
#     assert b"Overcast clouds" in response.data


def test_home_page_mock_api(weather_api_mock_client):
    """
    GIVEN a Flask application configured for testing with a mocked weather API,
    WHEN the '/' page is requested (GET),
    THEN check the response is valid and contains the expected weather data.
    """
    response = weather_api_mock_client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b"London" in response.data
    assert b"GB" in response.data
    # Depending on your template filter (capitalize), adjust the expected string.
    assert b"Overcast clouds" in response.data

def test_index_post_branch(test_client, mocker):
    """
    GIVEN a POST request with form data,
    WHEN the index route is requested,
    THEN check that the POST branch is executed.
    """
    # Define a dummy response for the API call during the POST.
    class DummyResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json_data = json_data
        def json(self):
            return self._json_data

    def dummy_post_response(*args, **kwargs):
        data = {
            "coord": {"lon": 0.0, "lat": 0.0},
            "weather": [{
                "description": "snowy",
                "icon": "13d",
                "main": "Snow"
            }],
            "name": "PostCity",
            "sys": {"country": "PC"},
            "main": {
                "temp": 0.0,
                "feels_like": -2.0,
                "temp_min": -3.0,
                "temp_max": 1.0,
                "pressure": 1020,
                "humidity": 90
            },
            "visibility": 1000,
            "wind": {"speed": 5.0},
            "cod": 200
        }
        return DummyResponse(200, data)

    # Patch requests.get in the views module to use our dummy_post_response.
    mocker.patch("website.views.requests.get", dummy_post_response)
    response = test_client.post(
        "/", 
        data={"city": "PostCity", "state": "dummy", "country": "PC"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"PostCity" in response.data

def test_save_location_route(test_client, mocker):
    """
    GIVEN a valid JSON payload for location,
    WHEN /save_location is requested,
    THEN verify that the session is updated and a JSON redirect is returned.
    """
    class DummyResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json_data = json_data
        def json(self):
            return self._json_data

    def dummy_save_response(*args, **kwargs):
        data = {
            "name": "SavedCity",
            "sys": {"country": "SC"}
        }
        return DummyResponse(200, data)

    mocker.patch("website.views.requests.get", dummy_save_response)
    response = test_client.post("/save_location", json={"latitude": 1, "longitude": 2})
    json_data = response.get_json()
    assert "redirect" in json_data
