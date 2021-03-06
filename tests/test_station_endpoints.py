from app.model import Station
import json


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


def test_create_station_success(my_test_client, get_token):
    """
    GIVEN an app configured for testing
    WHEN the '/api/stations' is passed (POST) with valid station json data
    THEN check that the response is valid and has a new station data
    """

    station_data = {"name": "Toronto Union", "location": "Dundas and Young"}
    resp = my_test_client.post(
        '/api/stations', json={**station_data}, headers={"Authorization": "Bearer {}".format(get_token)})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['name'] == "Toronto Union"


def test_create_station_error(my_test_client, get_token):
    """
    GIVEN an app configured for testing
    WHEN the '/api/stations' is passed (POST) with empty data
    THEN check that the response is 400
    """
    resp = my_test_client.post(
        '/api/stations', headers={"Authorization": "Bearer {}".format(get_token)})
    assert resp.status_code == 400


def test_update_station_success(my_test_client, get_token):
    """
    GIVEN an app configured for testing
    WHEN the '/api/stations' is passed (POST) with station json data
    THEN check that the response is valid and has a new station id is returned
    """
    _station = {'id': 1, 'name': 'updated station1',
                'location': "Toronto", 'date_created': '2021-01-20 23:38:01'}
    resp = my_test_client.post('/api/station/1', json={**_station}, headers={
                               "Authorization": "Bearer {}".format(get_token)})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['id'] == 1


def test_update_station_error(my_test_client, get_token):
    """
    GIVEN an app configured for testing
    WHEN the '/api/stations' is passed (POST) without date_created value
    THEN check that the response code is 422
    """
    _station = {'id': 1, 'name': 'updated station1',
                'location': "Toronto"}
    resp = my_test_client.post('/api/station/1', json={**_station}, headers={
                               "Authorization": "Bearer {}".format(get_token)})
    assert resp.status_code == 422
