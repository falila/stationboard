from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app.model import db, init_db
from flask_migrate import Migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    with app.app_context():
        init_db()

    from flask_restful import Api

    from app.api import bp as api_bp
    from app.api.stations import StationResource, StationsResource, StationTripResource
    from app.api.trips import TripResource, TripsResource
    api = Api(api_bp)
    api.add_resource(StationResource, '/station/<int:station_id>')
    api.add_resource(StationsResource, '/stations')
    api.add_resource(StationTripResource, '/station/<int:station_id>/trips')

    api.add_resource(TripResource, '/trip/<int:trip_id>')
    api.add_resource(TripsResource, '/trips')

    app.register_blueprint(api_bp, url_prefix='/api')

    return app
