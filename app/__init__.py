from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import ProdConfig
from app.model import db, init_db
from flask_migrate import Migrate
from app.api.auth import TokenRefresh
from flask_jwt_extended import JWTManager


def create_app(config_class=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']

        return app.model.RevokedTokenModel.is_jti_blacklisted(jti)

    with app.app_context():
        init_db()

    from flask_restful import Api

    from app.api import bp as api_bp
    from app.api.stations import StationResource, StationsResource, StationTripResource
    from app.api.trips import TripResource, TripsResource
    from app.api.auth import UserLogin, UserLogoutAccess, UserLogoutRefresh, UserRegistration, AllUsers, TokenRefresh

    api = Api(api_bp)
    api.add_resource(StationsResource, '/stations')
    api.add_resource(StationResource, '/station/<int:station_id>')
    api.add_resource(StationTripResource, '/station/<int:station_id>/trips')
    api.add_resource(TripResource, '/trip/<int:trip_id>')
    api.add_resource(TripsResource, '/trips')
    api.add_resource(AllUsers, '/users')

    from flask import Blueprint

    auth_bp = Blueprint('auth', 'authentication')
    auth_api = Api(auth_bp)
    auth_api.add_resource(UserRegistration, '/signup')
    auth_api.add_resource(UserLogin, '/login')
    # only access tokens are allowed
    auth_api.add_resource(UserLogoutAccess, '/logout/access')
    # only refresh tokens are allowed
    auth_api.add_resource(UserLogoutRefresh, '/logout/refresh')
    # only refresh tokens are allowed
    auth_api.add_resource(TokenRefresh, '/refresh')

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
