from unittest import TestCase
from app import create_app as app_init
import pytest
from config import TestingConfig


@pytest.fixture(scope='function')
@pytest.mark.skip
def create_test_app():
    return app_init(TestingConfig)


@pytest.mark.skip
def test_app_is_testing(create_test_app):
    app = create_test_app
    assert app.config['DEBUG'] is True
