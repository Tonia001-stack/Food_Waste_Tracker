from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config, ProductionConfig, DevelopmentConfig
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    
    # Auto-detect environment and use appropriate config
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(ProductionConfig)
        print("🚀 Using PRODUCTION configuration")
    else:
        app.config.from_object(DevelopmentConfig) 
        print("🔧 Using DEVELOPMENT configuration")
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    from app.routes import main, auth, food, donations
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(food.bp)
    app.register_blueprint(donations.bp)
    
    return app

# Import models here to avoid circular imports
from app.models import User, FoodItem, Donation, Achievement
