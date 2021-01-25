
import pytest
import json


def test_signup_success(my_test_client):
    """
    GIVEN an app configured for testing
    WHEN the '/auth/signup' is passed (POST) with user data
    THEN check that a new user is created and a token is returned
    """
    resp = my_test_client.post(
        '/auth/signup', json={'username': 'test', 'password': 'test'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data
    assert 'access_token' in data


def test_signup_failed(my_test_client):
    """
    GIVEN an app configured for testing
    WHEN the '/auth/signup' is passed (POST) with user data
    THEN check that a new user is created and a token is returned
    """
    resp = my_test_client.post(
        '/auth/signup', json={'username': 'test', '': 'test'})
    assert resp.status_code != 200


def test_login(my_test_client):
    """
    GIVEN an app configured for testing
    WHEN the '/auth/login' is passed (POST) with user data
    THEN check that a new user is authenticated and a token is returned
    """
    # registration
    resp = my_test_client.post(
        '/auth/signup', json={'username': 'bob', 'password': 'bobpassword'})
    assert resp.status_code == 200
    # login
    resp = my_test_client.post(
        '/auth/login', json={'username': 'bob', 'password': 'bobpassword'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'access_token' in data
