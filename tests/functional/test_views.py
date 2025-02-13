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
    assert b"Overcast clouds" in response.data