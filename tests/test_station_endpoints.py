from app import create_app
from config import TestingConfig
from app.model import Station
import pytest
import json


@pytest.fixture(scope='module')
def my_test_client():
    app = create_app(TestingConfig)

    # Creating our testing client
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


def test_get_stations(my_test_client):
    """
    GIVEN an app configured for testing
    WHEN the '/api/stations' is passed (GET)
    THEN check that the response is valid and contents 10 stations
    """
    resp = my_test_client.get('/api/stations')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data
    assert len(data) == 10


def test_create_station_succes(my_test_client):
    """
    GIVEN an app configured for testing
    WHEN the '/api/stations' is passed (POST) with valid station json data
    THEN check that the response is valid and has a new station data
    """
    station_data = {"name": "Toronto Union", "location": "Dundas and Young"}
    resp = my_test_client.post(
        '/api/stations', json={**station_data})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['name'] == "Toronto Union"


def test_create_station_error(my_test_client):
    """
    GIVEN an app configured for testing
    WHEN the '/api/stations' is passed (POST) with empty data
    THEN check that the response is valid and has a new station data
    """
    resp = my_test_client.post('/api/stations')
    assert resp.status_code == 400
