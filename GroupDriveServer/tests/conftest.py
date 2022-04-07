import pytest
from app import create_app


@pytest.fixture()
def app():
    app = create_app("test_config.py")
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()
