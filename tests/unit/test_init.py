from website import create_app

def test_create_app():
    app = create_app()
    assert app is not None
    # Verify that a secret key is set.
    assert "SECRET_KEY" in app.config
