from app import create_app
from config import TestingConfig
import pytest


@pytest.fixture(scope='session')
def my_test_client():
    app = create_app(TestingConfig)

    # Creating our testing client
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


@pytest.fixture(scope='session')
def get_token(my_test_client):
    """
    GIVEN an app configured for testing
    WHEN the '/auth/signup' is passed (POST) with user data
    THEN check that a new user is created and a token is returned
    """
    resp = my_test_client.post(
        '/auth/signup', json={'username': 'testuser', 'password': 'test'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'access_token' in data
    return data['access_token']
