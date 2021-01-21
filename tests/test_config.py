from unittest import TestCase
from app import create_app as app_init


@pytest.fixtures
def create_test_app():
    return app_init('stationboard.config.TestingConfig')


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        return app_init('stationboard.config.DevelopmentConfig')

    def test_app_is_development(self):
        app = self.create_app()
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(app is None)


def test_app_is_testing(create_test_app):
    app = create_test_app
    assert app.config['DEBUG']
