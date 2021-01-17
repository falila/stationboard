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
    from app.api.stations import StationResource, StationsResource
    api = Api(api_bp)
    api.add_resource(StationResource, '/station/<int:station_id>')
    api.add_resource(StationsResource, '/stations')

    app.register_blueprint(api_bp, url_prefix='/api')

    return app
