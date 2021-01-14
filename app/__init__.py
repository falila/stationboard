from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db = SQLAlchemy(app)
    ma = Marshmallow(app)

    from flask_restful import Api
    
    from app.api import bp as api_bp
    from app.api.stations import Station , Stations
    api = Api(api_bp)
    api.add_resource(Station, '/station/<int:station_id>')
    api.add_resource(Stations, '/stations')

    app.register_blueprint(api_bp, url_prefix='/api')

    return app


from app import model 
