from flask import Flask
from datetime import datetime, timezone, timedelta
from app.extensions import db
from config import Config
from flask_migrate import Migrate
from app.models import *
from flask_jwt_extended import JWTManager
from app.main.auth.api.blueprints.auth import auth
from app.main.designs.api.blueprints.designs import designs
from app.main.assets.api.blueprints.assets import assets


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth, url_prefix = '/api/auth')
    app.register_blueprint(designs, url_prefix = '/api/designs')
    app.register_blueprint(assets, url_prefix = '/api/assets')
    
    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app