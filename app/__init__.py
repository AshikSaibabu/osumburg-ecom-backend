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
from app.main.categories.api.blueprints.categories import categories
from app.main.color_variants.api.blueprints.color_variants import color_variant
from app.main.type.api.blueprints.type import type
from app.main.products.api.blueprints.products import product
from app.main.size_variants.api.blueprints.size_variants import size_variants
from app.main.sleeve_length_variant.api.blueprints.sleeve_length_variant import sleeve_length_variants
from app.main.product_color_variants.api.blueprints.product_color_variants import product_color_variants
from app.main.product_color_variant_images.api.blueprints.product_color_variant_images import product_color_variant_images
from app.main.product_variants.api.blueprints.product_variants import product_variant
from app.main.stock.api.blueprints.stock import stock


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
    app.register_blueprint(categories, url_prefix = '/api/categories')
    app.register_blueprint(color_variant, url_prefix = '/api/color_variant')
    app.register_blueprint(type, url_prefix = '/api/type')
    app.register_blueprint(product, url_prefix = '/api/product')
    app.register_blueprint(size_variants, url_prefix = '/api/size_variants')
    app.register_blueprint(sleeve_length_variants, url_prefix = '/api/sleeve_length_variants')
    app.register_blueprint(product_color_variants, url_prefix = '/api/product_color_variants')
    app.register_blueprint(product_color_variant_images, url_prefix = '/api/product_color_variant_images')
    app.register_blueprint(product_variant, url_prefix = '/api/product_variant')
    app.register_blueprint(stock, url_prefix = '/api/stock')
    
    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app